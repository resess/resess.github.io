---
layout: default
title: ViaLin Implementation
nav_order: 3
has_children: false
permalink: /docs/artifact
---

# ViaLin Implementation
---

This page describes how to install and run ViaLin. 

1. Install and build Android AOSP version 8.0.0 by following the instructions in the [Android manual](https://source.android.com/docs/setup/build/building) (in our evaluation, we targeted android-8.0.0_r21, lunch 31).

2. Download the [artifact](../data/ViaLinArtifact.zip) and unpack it to vialin/

3. Change the directory to path-taint folder, then build the tool with ``mvn package install``

4. Copy vialin/android-src/openjdk_java_files.mk to [AOSP]/libcore/openjdk_java_files.mk

5. Copy vialin/android-src/droiddoc.mk to [AOSP]/build/make/core/droiddoc.mk

6. Copy vialin/android-src/droiddoc_core.mk to [AOSP]/build/core/droiddoc.mk

7. Copy vialin/android-src/java.mk to [AOSP]/build/core/java.mk

8. Copy vialin/android-src/Thread.java to [AOSP]/libcore/ojluni/src/main/java/java/lang/Thread.java

9. Copy vialin/android-src/PathTaint.java to [AOSP]/libcore/ojluni/src/main/java/java/lang/PathTaint.java

10. Copy vialin/android-src/TaintDroid.java to [AOSP]/libcore/ojluni/src/main/java/java/lang/TaintDroid.java

11. Copy vialin/android-src/instruction_builder.cc to [AOSP]/art/compiler/optimizing/instruction_builder.cc

12. Copy vialin/android-src/java_lang_Thread.cc to [AOSP]/art/runtime/native/java_lang_Thread.cc


13. Copy vialin/android-src/register_line-inl.h to [AOSP]/art/runtime/verifier/register_line-inl.h

14. Copy vialin/android-src/method_verifier.cc to [AOSP]/art/runtime/verifier/method_verifier.cc 

15. Copy vialin/android-src/register_line.cc to [AOSP]/art/runtime/verifier/register_line.cc 

16. Copy vialin/android-src/class_linker.cc to [AOSP]/art/runtime/class_linker.cc 

17. Replace [path-to-jar] in java.mk to the jar file built from step #3

18. Create a folder called ``framework_analysis_results``, place its path in [framework_analysis_results] in the java.mk

19. Create folder class_info/ inside ``framework_analysis_results``

20. Replace [path-to-sources] ang [path-to-sink] in java.mk with path to the absolute path of ``GPBench/config/empty.txt`` from the evaluation package


21. Change the directory to the [AOSP], follow the "Setting up the environment", "Choosing a target", and "Building the code" section of the [Building Android Manual](https://source.android.com/docs/setup/build/building)

22. Flash an Android device by following the instructions in the Android Manual [Flashing Devices](https://source.android.com/docs/setup/build/running)

23. An example on how to taint and install an app on the device is in the evaluation package ``GPBench/scripts/run_gp.py``, run from the vialin directory ``python3 GPBench/scripts/run_gp.py``, modify the paths in the script to point to the correct folder for the AOSP, ``framework_analysis_results``, source/sink lists, the android-record-and-replay tool included in vialin, and the path to the apk.

