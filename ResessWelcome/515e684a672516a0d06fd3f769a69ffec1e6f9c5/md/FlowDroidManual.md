# Overview

This guide provides details on how to run FlowDroid (as well as its plugin IccTA) under certain configurations.

# Dependencies

## FlowDroid (with IccTA)

There are two repositories for FlowDroid.
- The current version which is under development is for FlowDroid 2.5 or later: [GitHub](https://github.com/secure-software-engineering/FlowDroid) (escpecially its [develop branch](https://github.com/secure-software-engineering/FlowDroid/tree/develop) if you need to modify its source code) and [releases/pre-built binaries](https://github.com/secure-software-engineering/FlowDroid/tree/develop) (if you only need to run FlowDroid using command line).
- There is also a legacy version of FlowDroid, which is NOT recommended to use from command line. In this manual, we also do NOT provide configurations for this legacy version.
  - The best way to use it is via pre-built binaries. Check its [Wiki](https://github.com/secure-software-engineering/soot-infoflow-android/wiki) to download all pre-built binaries.
  - To run it via souce code, you need to clone the following dependencies: [Jasmin](https://github.com/Sable/jasmin), [Heros](https://github.com/Sable/heros), [Soot](https://github.com/Sable/soot), [soot-infoflow](https://github.com/secure-software-engineering/soot-infoflow), [soot-infoflow-android](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links). Notice that it is not graranteed that the latest version of these dependencies are compatible to each other.

IccTA is already embedded inside both versions of FlowDroid, so it is not necessary to download it.

## IC3

In order to use IccTA inside FlowDroid to enable analysis on Inter Component Communication (ICC), IC3 is needed: [GitHub](https://github.com/siis/ic3) and its [home page](http://siis.cse.psu.edu/ic3/). However, the version provided from the above sources is not the latest one and may contain potential bugs. You can find the latest version on **Zeus**, under folder **/data/common/IC3/**. There are two JAR files: *ic3-0.2.0-full.jar* and *RetargetedApp.jar*.

## Android Platforms (android.jar)

Android platform files (android.jar) are used in almost every step of FlowDroid. You can find it on **Zeuz**, under folder **/data/common/android_platforms**. This folder contains many sub-folders for different API levels of Android framework (currently 7 to 28). For the following instructions, */path/to/android.jar* means you need to select an android.jar for a specific API level; */path/to/android/platforms/* means you can use */data/common/android_platforms* directly.

# Instructions

## IC3

IC3 consists of two steps:
- Retargeting an app to a given API level:
```bash
java [option] -jar RetargetedApp.jar /path/to/android.jar /path/to/apk /path/to/temp/dir/for/retargeted/files/ [> /path/to/log/file]
```
- Generating ICC model for the app:
```bash
java [option] -jar ic3-0.2.0-full.jar -apkormanifest /path/to/apk -input /path/to/temp/dir/for/retargeted/files/ -cp /path/to/android.jar -protobuf /path/to/temp/dir/for/iccmodel/ [> /path/to/log/file]
```
Notice that you need to create two temporary folders: */path/to/temp/dir/for/retargeted/files/* and */path/to/temp/dir/for/iccmodel/*. The resultant ICC model for the app is generated under */path/to/temp/dir/for/iccmodel/* as a TXT file. **The TXT file will be overriden the next time you run IC3 for another app, so please remember to move it if you need to keep it.**

## FlowDroid (with IccTA)