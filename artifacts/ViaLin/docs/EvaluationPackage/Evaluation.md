---
layout: default
title: Evaluation Package
nav_order: 4
has_children: false
permalink: /docs/eval
---

# Evaluation Package


This page describes both the [DroidICCBench](#droidiccbench) and the [GPBench](#GPBench) benchmarks along with the configuration used to run the benchmarks.
The evaluation package scripts and configuration files can be downloaded [here](../data/evaluation_package.zip)

This package is organized in the following structure:
```
.
├── android-record-replay/
├── DroidICCBench/
│   ├── scripts/
│   │   ├── run_droidbench.py
│   │   └── translate_droidbench.py
│   └── config/
│       ├── app1.src.log
│       ├── app1.sink.log
│       └── ...
└── GPBench/
    ├── scripts/
    │   ├── run_gp.py
    │   ├── run_overhead.py
    │   └── translate_gp.py
    └── config/
        ├── app1.src.log
        ├── app1.sink.log
        └── ...
```

The apps can be downloaded [here](https://www.mediafire.com/file/7sz884kfqw2w85q/apps.zip/file)

The apps package is organized in the following structure:
```
.
├── DroidICCBench/
│   └── apps/
│       ├── Category1/
│       │   ├── app1
│       │   ├── app2
│       │   └── ...
│       ├── Category2/
│       └── ...
└── GPBench/
    └── apps/
        ├── app1
        ├── app2
        └── ...
```



The evaluation package contains the ```android-touch-record-replay``` tool which we used to record and replay the execution for each app.

Next, we describe the DroidICCBench and GPBench sections of the evaluation package.

---

## DroidICCBench

### Apps
The benchmark consists of 217 apps from [DroidBench](https://github.com/secure-software-engineering/DroidBench/tree/develop) and [ICCbench](https://github.com/fgwei/ICC-Bench). We had to exclude eight
apps for which we cannot reliably trigger the flow in an automated
way, e.g., because it is triggered when the phone memory is low.
The 8 eight excluded apps are:

1. Callbacks.AnonymousClass1
2. Callbacks.LocationLeak1
3. Callbacks.LocationLeak2
4. Callbacks.LocationLeak3
5. Callbacks.RegisterGlobal1
6. Callbacks.RegisterGlobal2
7. GeneralJava.FactoryMethods1
8. Lifecycle.ActivityLifecycle3

For the remaining 209 apps, as the benchmark apps were developed for an older Android API (level 19), where permissions to run any sensitive, we modified the apps to request permissions using the approach if the newer Android versions. At the end, we used 209 apps in our evaluation. The apps are grouped into categories under the ``` DroidICCBench/apps ``` folder.

### Configuration

The combined sources list is under ``` DroidICCBench/config/source_full_list.txt ```, the combined sinks list is under ``` DroidICCBench/config/sinks_full_list.txt ```.
The replay script for each app is at ``` DroidICCBench/config/[app].replay.txt ```, apps without an execution script use the default script ``` DroidICCBench/config/trigger_flow.replay.txt ```.

### Replication
The script ``` DroidICCBench/scripts/run_droidbench.py ``` runs the specified benchmark app by selecting its number, the number of each benchmark is its line number in the ``` DroidICCBench/config/droidbench_apks.log```. The script ``` DroidICCBench/scripts/translate_droidbench.py ``` extracts the paths from the Android logcat and translates it into a human readable format.

---
## GPBench
### Apps
We used the benchmark of Google Play applications from Zhang et al [37]. We excluded from our study three out of the 19 apps, as their backend servers were non-functional at the time of writing and we thus could not execute them dynamically. The remaining 16 apps are listed below:

<img src="https://anonforreview.github.io//SupplementaryMaterials/img/subjects.png" alt="drawing" width="400"/>



### Configuration

The sources short list for each app ``` GPBench/config/[app-name].src.log ```, the sinks short list for each app is under ``` GPBench/config/[app-name].sink.log ```.
The long list of sources is at ``` GPBench/config/source_long_list.txt ``` and the long list of sinks is ``` GPBench/config/sinks_long_list.log ```.
The replay script for each app is at ``` GPBench/config//[app].replay.txt ```.


### Replication

The script ``` GPBench/scripts/run_gp.py ``` runs the specified benchmark app.
The script ``` GPBench/scripts/run_overhead.py ``` runs the overhead experiment.
The script ``` GPBench/scripts/translate_gp.py ``` extracts the paths from the Android logcat and translates it into a human readable format.


---
## Fake WhatsApp client
### App
We cannot distribute the YoWhatsApp malicious apk online, instead, we provide its following indicators:

package name: com.gbbwhatsapp

sha1 hash: a8dbfd8d48e4a4952e1a822ce1323a37348f0c1c

sha256 hash: 89c23dc02f4f67972a5c4cd9ccc61f7c08c95173d07a980c7340101ba597939e

md5: 531d0a00d3b7221b4ac712fbfe846029

blog describing the malware: [link](https://securelist.com/malicious-whatsapp-mod-distributed-through-legitimate-apps/107690/)

### Sources and Sinks

- Sources configuration [file](../data/YoWhatsApp.src.txt)
- Sink configuration [file](../data/YoWhatsApp.sink.txt)

### ViaLin Path

The path provided to the analysts is available [here](../data/YoWhatsAppPath.log)

