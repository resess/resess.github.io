---
layout: default
title: Benchmarks
nav_order: 3
has_children: false
permalink: /docs/benchmarks
---

# Benchmarks Used in Evaluation
---

The table below contains the original and the instrumented versions of each benchmark application used in the evaluation of Kuber. 
In our instrumentation, we added traces to each API to calculate the execution time of the API while subtracting the execution times of the APIs it triggers. 

|Benchmark Name|Number of Services| Orginal Repo | Changed Repo|
|:-------------------------------|:------------------:|
|Hotel Reservation|8|[link](https://github.com/delimitrou/DeathStarBench/tree/master/hotelReservation)|[link](https://github.com/kubercostoptimizer/Kuber/tree/master/code/apps/hotel-reservation/code)
|Media Microsvc|11|[link](https://github.com/delimitrou/DeathStarBench/tree/master/mediaMicroservices)|[link](https://github.com/kubercostoptimizer/Kuber/tree/master/code/apps/media-microsvc/code)
|Social Network|12|[link](https://github.com/delimitrou/DeathStarBench/tree/master/hotelReservation)|[link](https://github.com/kubercostoptimizer/Kuber/tree/master/code/apps/social-network/code)
|Sockshop|7|[link](https://github.com/microservices-demo)|[link](https://github.com/kubercostoptimizer/Kuber/tree/master/code/apps/sock-shop/code)


An example of the instrumented GET API of the Catalogue service in the SockShop application is below. 
Here, we subtract the response time of the database call from the API execution time.
``` go
 
 // Original API definition
func (s *catalogueService) Get(id string) (Sock, error) {   
        // other code
        err := s.db.Get(&sock, query, id)
        // other code
        return sock, nil
}
 
 // API definition with execution time calculations 
func (s *catalogueService) Get(id string) (Sock, error) {
      start := time.Now() // <- Start Timer for API Total Execution time
      elapsed_external_call_time := time.Duration(0)
      span := opentracing.StartSpan("Get")

      // Other code
 
      external_call_2 := time.Now()
      err := s.db.Get(&sock, query, id)  // <- External Call
      elapsed_external_call_time = elapsed_external_call_time + time.Since(external_call_2)

      // Other code
      
      elapsed := time.Since(start) // <- end Timer for API Total Execution time
      elapsed = elapsed - elapsed_external_call_time
      span.LogKV("runtime_ms",float64(elapsed)/float64(time.Millisecond)) // <- send data to Istio
      span.Finish()
      return sock, nil
}

```

