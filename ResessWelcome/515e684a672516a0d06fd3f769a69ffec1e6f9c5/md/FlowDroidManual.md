# Overview

This guide provides details on how to run FlowDroid (as well as its plugin IccTA) under certain configurations. Since FlowDroid depends on Soot for some operations (e.g. converting DEX files to JIMPLE files, generating call graph (CG)), this guide also provides some instructions on how to use Soot for specific purposes.

# Dependencies

## FlowDroid (with IccTA)

There are two repositories for FlowDroid.
- The current version which is under development is for FlowDroid 2.5 or later: [GitHub](https://github.com/secure-software-engineering/FlowDroid) (escpecially its [develop branch](https://github.com/secure-software-engineering/FlowDroid/tree/develop) if you need to modify its source code) and [releases/pre-built binaries](https://github.com/secure-software-engineering/FlowDroid/tree/develop) (if you only need to run FlowDroid using command line).
- There is also a legacy version of FlowDroid, which is NOT recommended to use from command line.
  - The best way to use it is via pre-built binaries. Check its [Wiki](https://github.com/secure-software-engineering/soot-infoflow-android/wiki) to download all pre-built binaries.
  - To run it via souce code, you need to clone the following dependencies: [Jasmin](https://github.com/Sable/jasmin), [Heros](https://github.com/Sable/heros), [Soot](https://github.com/Sable/soot), [soot-infoflow](https://github.com/secure-software-engineering/soot-infoflow), [soot-infoflow-android](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links). Notice that it is not graranteed that the latest version of these dependencies are compatible to each other.

IccTA is already embedded inside both versions of FlowDroid, so it is not necessary to download it.

## IC3

In order to use IccTA inside FlowDroid to enable analysis on Inter Component Communication (ICC), IC3 is needed: [GitHub](https://github.com/siis/ic3) and its [home page](http://siis.cse.psu.edu/ic3/). However, the version provided from the above sources is not the latest one and may contain potential bugs. You can find the latest version on **Zeus**, under folder **/data/common/IC3/**. There are two JAR files: *ic3-0.2.0-full.jar* and *RetargetedApp.jar*.

## Android Platforms (android.jar)

Android platform files (android.jar) are used in almost every step of FlowDroid. You can find it on **Zeus**, under folder **/data/common/android_platforms/**. This folder contains many sub-folders for different API levels of Android framework (currently 7 to 28). For the following instructions, */path/to/android.jar* means you need to select an android.jar for a specific API level; */path/to/android/platforms/* means you can use */data/common/android_platforms/* directly.

## Soot

FlowDroid now builds with Maven, which takes care of the dependencies automatically.
You do not have to handle the Soot dependency yourself when using FlowDroid.

[Soot](https://github.com/Sable/soot) is the basic analysis framework, and FlowDroid normally pulls a version from the Soot maven repository. The version is declared in the pom file.

# Instructions

## IC3

We describe how to use IC3 first, as IccTA in FlowDroid needs the output of IC3. IC3 consists of two steps:
1. Retargeting an app to a given API level:
```bash
java [options] -jar RetargetedApp.jar /path/to/android.jar /path/to/apk /path/to/temp/dir/for/retargeted/files/ [> /path/to/log/file]
```
2. Generating ICC model for the app:
```bash
java [options] -jar ic3-0.2.0-full.jar -apkormanifest /path/to/apk -input /path/to/temp/dir/for/retargeted/files/ -cp /path/to/android.jar -protobuf /path/to/temp/dir/for/iccmodel/ [> /path/to/log/file]
```
Notice that you need to create two temporary folders: */path/to/temp/dir/for/retargeted/files/* and */path/to/temp/dir/for/iccmodel/*. The resultant ICC model for the app is generated under */path/to/temp/dir/for/iccmodel/* as a TXT file. **The TXT file will be overriden the next time you run IC3 for another app, so please remember to move it if you need to keep it.**

## FlowDroid (with IccTA)

In this section, we will discuss how to run FlowDroid via command line, and provide possible parameters to configure the analysis.

### Version Under Development

#### Basic Command
```bash
java [options] -jar /path/to/soot-infoflow-cmd-jar-with-dependencies.jar -a /path/to/apk -p [/path/to/android/platforms/ (recommended) or /path/to/android.jar] [args]
```

#### Frequently-used Arguments: Basic Taint Analysis

**TODO (The following is just a sample)** 

| Option | Description | Default | Recommendation (if different to default) |
|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| sourcessinksfile | Definition file for sources and sinks. | null | **You must set it to a file with proper sources and sinks. A sample of   file with sources and sinks can be found   [here](https://resess.github.io/ResessWelcome/515e684a672516a0d06fd3f769a69ffec1e6f9c5/attachments/SourcesAndSinks.txt).** |
| enablereflection | Enable support for reflective method   calls. |  |  |
| taintwrapper | Use the specified taint wrapper   algorithm (NONE, EASY, STUBDROID, MULTI). **Note: NONE: No taint wrapper,   EASY: Use taint wrappers defined in *taintwrapperfile*, STUBDROID: Use   definitions defined in *taintwrapperfile*, MULTI: Use multiple definition files   defined in *taintwrapperfile*.** | If *taintwrapperfile* is defined:   MULTI. If *taintwrapperfile* is not defined: DEFAULT. | Do not modify the default value of it or set it to EAST with   *taintwrapperfile* set to a file with easy taint wrappers. |
| taintwrapperfile | Definition file for the taint wrapper. | null | Set it to the file with easy taint wrappers when *taintwrapper* is set to   EASY. |
| logsourcesandsinks | Write the discovered sources and   sinks to the log output. |  |  |
| cgalgo | Callgraph algorithm to use (AUTO,   CHA, VTA, RTA, SPARK, GEOM). |  |  |
| implicit | Use the specified mode when   processing implicit data flows (NONE, ARRAYONLY, ALL). |  |  |

#### Frequently-used Arguments: ICC-related

**TODO (The following is just a sample)** 

| Option | Description | Default | Recommendation (if different to default) |
|--------------------|------------------------------------------------------------------------------------------------------------|---------|------------------------------------------|
| iccmodel | File containing the inter-component   data flow model (ICC model). |  |  |
| noiccresultspurify | Do not purify the ICC results, i.e.,   do not remove simple flows that also have a corresponding ICC flow. |  |  |

#### Other Arguments (NOT recommended to modify)

**TODO (The following is just a sample)** 

| Option | Description | Default | Recommendation (if different to default) |
|----------------------------|-----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------|------------------------------------------|
| configfile | Use the given configuration file. | Defined in   loadConfigurationFile.java of soot-infoflow-android. |  |
| outputfile | Output XML file for the discovered   data flows. **Note: it must be a directory when analyzing multiple APKs.** | null |  |
| additionalclasspath | Additional JAR file that shal be put on the classpath. | null |  |
| skipapkfile | APK file to skip when processing a directory of input files. | null |  |
| timeout | Timeout for the main data flow analysis. | null |  |
| callbacktimeout | Timeout for the callback collection phase. | null |  |
| resulttimeout | Timeout for the result collection   phase. |  |  |
| nostatic | Do not track static data flows. |  |  |
| nocallbacks | Do not analyze Android callbacks. |  |  |
| noexceptions | Do not track taints across   exceptional control flow edges. |  |  |
| notypechecking | Disable type checking during taint   propagation. |  |  |
| missingsummariesoutputfile | Outputs a file with information   about which summaries are missing. |  |  |
| aplength | Maximum access path length. |  |  |
| nothischainreduction | Disable reduction of inner class   chains. |  |  |
| aliasflowins | Use a flow-insensitive alias   analysis. |  |  |
| paths | Compute the taint propagation paths   and not just source-to-sink connections. This is a shorthand notation for -pr   fast. |  |  |
| maxthreadnum | Limit the maximum number of threads   to the given value. |  |  |
| onecomponentatatime | Analyze one Android component at a   time. |  |  |
| onesourceatatime | Analyze one source at a time. |  |  |
| sequentialpathprocessing | Process the result paths   sequentially instead of in parallel. |  |  |
| singlejoinpointabstraction | Only use a single abstraction at   join points, i.e., do not support multiple sources for one value. |  |  |
| maxcallbackspercomponent | Eliminate Android components that   have more than the given number of callbacks. |  |  |
| maxcallbacksdepth | Only analyze callback chains up to   the given depth. |  |  |
| mergedexfiles | Merge all dex files in the given APK   file into one analysis target. |  |  |
| pathspecificresults | Report different results for same   source/sink pairs if they differ in their propagation paths. |  |  |
| layoutmode | Mode for considerung layout controls   as sources (NONE, PWD, ALL). |  |  |
| pathalgo | Use the specified algorithm for   computing result paths (CONTEXTSENSITIVE, CONTEXTINSENSITIVE, SOURCESONLY). |  |  |
| callbackanalyzer | Use the specified callback analyzer   (DEFAULT, FAST). |  |  |
| dataflowsolver | Use the specified data flow solver   (CONTEXTFLOWSENSITIVE, FLOWINSENSITIVE). |  |  |
| aliasalgo | Use the specified aliasing algorithm   (NONE, FLOWSENSITIVE, PTSBASED, LAZY). |  |  |
| codeelimination | Use the specified code elimination   algorithm (NONE, PROPAGATECONSTS, REMOVECODE). |  |  |
| callbacksourcemode | Use the specified mode for defining   which callbacks introduce which sources (NONE, ALL, SOURCELIST). |  |  |
| pathreconstructionmode | Use the specified mode for   reconstructing taint propagation paths (NONE, FAST, PRECISE). |  |  |
| staticmode | Use the specified mode when tracking   static data flows (CONTEXTFLOWSENSITIVE, CONTEXTFLOWINSENSITIVE, NONE). |  |  |
| analyzeframeworks | Analyze the full frameworks together   with the app without any optimizations. |  |  |

### Legacy Version

**TODO** 

## Soot
Soot is a Java optimization framework that can be used as the basis for purforming program analysis on Java programs (e.g. Android apps are written in Java).

Normally, we include Soot as a module and use the APIs to access the basic functionalities.

### Running Soot through command line

Altough Soot is normally included as a module in your project, there could be some rare cases that you would like to invoke Soot from command line.

Then, Soot is invoked as follows:

```java
java javaOptions soot.Main [ sootOption* ] classname*
```


### Including Soot in your Project

A Soot dependency can be added via Maven, Gradle, SBT, etc using the following coordinates:

```xml
<dependencies>
  <dependency>
    <groupId>ca.mcgill.sable</groupId>
    <artifactId>soot</artifactId>
    <version>3.3.0</version>
  </dependency>
</dependencies>
```

### Basic options

#### General
|||
|--- |--- |
|-coffi|Use the good old Coffi front end for parsing Java bytecode (instead of using ASM).|
|-jasmin-backend|Use the Jasmin back end for generating Java bytecode (instead of using ASM).|
|-h -help|Display help and exit|
|-pl -phase-list|Print list of available phases|
|-ph phase-phase-help phase|Print help for specified
               phase|
|-version|Display version information and exit|
|-v -verbose|Verbose mode|
|-interactive-mode|Run in interactive mode|
|-unfriendly-mode|Allow Soot to run with no command-line options|
|-app|Run in application mode|
|-w -whole-program|Run in whole-program mode|
|-ws -whole-shimple|Run in whole-shimple mode|
|-fly -on-the-fly|Run in on-the-fly mode|
|-validate|Run internal validation on bodies|
|-debug|Print various Soot debugging info|
|-debug-resolver|Print debugging info from SootResolver|
|-ignore-resolving-levels|Ignore mismatching resolving levels|

**TODO** 