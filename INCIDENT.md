# Incident Report

## What happened

The application suffered from a performance degradation and outage for 8 minutes because of heavy intensive background operation.

## Timeline
The app was working good unitl 2.13 , it was then when the response time was elevated and the app started to respond very slowly. Health checks were passing.
It went on to increasse and went beyond teh threshold which was 50 ms. Response times start climbing and A POST /shorten request jumps from 11ms to 87ms, and then 134ms. Health checks still pass but report that Redis is "slow."

At 2.16 a Warning Triggered and it was " Redis BGSAVE in progress"
At 2:16:18 Latency spiked to 523 ms saying performance may be degraded

BGSAVE process led the latency to peak over 1500ms. Because the database is bottlenecked, the application API endpoints take far too long to respond.

By 02:18:15, requests start hitting a hard 2-second limit and fail completely, returning 504 gateway timeout errors. This continued till 2:21 and redis was unresponsive.

At 02:21:18 we had Redis BGSAVE completed - disk I/O returning to normal. This is when the heavy activity stopeed and atency stared to drop 834ms ➔ 423ms ➔ 198ms ➔ 89ms.

By 02:24:30, request times drop back down to 45ms, and soon settle back into the healthy 7–14ms range.


## Root cause

This situation happened because of the BGSAVE process. This process takes a snapshot and saves it to the disk in and it is very resource intensive process. It uses a lot of CPU and I/O resources, which can cause the application to slow down.

## Impact

The impact was that the application was not able to respond to the requests and the health checks were failing. Users experienced incredibly slow response times, eventually resulting in 504 Gateway Timeout errors.

## How to prevent this in the future

# Monitoring

1. Since in BGSAVE I/O is heavily used we can monitor iowait pecentage and then is iowait spikes we can say that the CPU is idle waiting for disk I/O to complete.
2. We can set up alerts if the Redis command latency is greater than 50ms for 30 seconds 
3. We can set up alerts if the API response time is greater than 500ms for 30 seconds 
4. We can set up alerts if the Redis BGSAVE process is in progress for more than certain time 
5. If data is not that critical we can disable periodic BGSAVE

# Changes to prevent this in future
we can intoduce a replica and then we can configure the replica to perform the BGSAVE disk writes. The master node will handle the in memory read and the writes . This will result in MAster node never touching the disk and hence response time is never delayed.

Also we can set up cron job to Schedule the BGSAVE run via redis-cli (the issue would be what is we set cron job at 3 am considering it a low traffic period but server crashes at 2pm so the data between 3 am to 2pm would be lost)

Implement a Circuit Breaker: If our application detects that Redis latency is consistently high (e.g., > 100ms), the circuit breaker should "trip." Instead of making users wait 2 seconds and getting a 504 error, the application immediately returns a graceful 503 Service Unavailable or a custom "We are experiencing heavy load" message. This prevents your server's connection pool from being exhausted.

