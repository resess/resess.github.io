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

```bash
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

<table>
    <tbody>
        <tr>
            <td><tt>-coffi </tt><br></td>
            <td colspan="2">Use the good old Coffi front end for parsing Java bytecode (instead of using ASM).</td>
        </tr>
        <tr>
            <td><tt>-jasmin-backend </tt><br></td>
            <td colspan="2">Use the Jasmin back end for generating Java bytecode (instead of using ASM).</td>
        </tr>
        <tr>
            <td><tt>-h </tt><br><tt>-help </tt><br></td>
            <td colspan="2">Display help and exit</td>
        </tr>
        <tr>
            <td><tt>-pl </tt><br><tt>-phase-list </tt><br></td>
            <td colspan="2">Print list of available phases</td>
        </tr>
        <tr>
            <td><tt>-ph <var>phase</var></tt><br><tt>-phase-help <var>phase</var></tt><br></td>
            <td colspan="2">Print help for specified
               <var>phase</var>
            </td>
        </tr>
        <tr>
            <td><tt>-version </tt><br></td>
            <td colspan="2">Display version information and exit</td>
        </tr>
        <tr>
            <td><tt>-v </tt><br><tt>-verbose </tt><br></td>
            <td colspan="2">Verbose mode</td>
        </tr>
        <tr>
            <td><tt>-interactive-mode </tt><br></td>
            <td colspan="2">Run in interactive mode</td>
        </tr>
        <tr>
            <td><tt>-unfriendly-mode </tt><br></td>
            <td colspan="2">Allow Soot to run with no command-line options</td>
        </tr>
        <tr>
            <td><tt>-app </tt><br></td>
            <td colspan="2">Run in application mode</td>
        </tr>
        <tr>
            <td><tt>-w </tt><br><tt>-whole-program </tt><br></td>
            <td colspan="2">Run in whole-program mode</td>
        </tr>
        <tr>
            <td><tt>-ws </tt><br><tt>-whole-shimple </tt><br></td>
            <td colspan="2">Run in whole-shimple mode</td>
        </tr>
        <tr>
            <td><tt>-fly </tt><br><tt>-on-the-fly </tt><br></td>
            <td colspan="2">Run in on-the-fly mode</td>
        </tr>
        <tr>
            <td><tt>-validate </tt><br></td>
            <td colspan="2">Run internal validation on bodies</td>
        </tr>
        <tr>
            <td><tt>-debug </tt><br></td>
            <td colspan="2">Print various Soot debugging info</td>
        </tr>
        <tr>
            <td><tt>-debug-resolver </tt><br></td>
            <td colspan="2">Print debugging info from SootResolver</td>
        </tr>
        <tr>
            <td><tt>-ignore-resolving-levels </tt><br></td>
            <td colspan="2">Ignore mismatching resolving levels</td>
        </tr>
    </tbody>
</table>

#### Input

<table>
    <tbody>
        <tr>
            <td><tt>-cp <var>path</var></tt><br><tt>-soot-class-path <var>path</var></tt><br><tt>-soot-classpath <var>path</var></tt><br></td>
            <td colspan="2">Use
               <var>path</var>
               as the classpath for finding classes.
            </td>
        </tr>
        <tr>
            <td><tt>-pp </tt><br><tt>-prepend-classpath </tt><br></td>
            <td colspan="2">Prepend the given soot classpath to the default classpath.</td>
        </tr>
        <tr>
            <td><tt>-ice </tt><br><tt>-ignore-classpath-errors </tt><br></td>
            <td colspan="2">Ignores invalid entries on the Soot classpath.</td>
        </tr>
        <tr>
            <td><tt>-process-multiple-dex </tt><br></td>
            <td colspan="2">Process all DEX files found in APK.</td>
        </tr>
        <tr>
            <td><tt>-search-dex-in-archives </tt><br></td>
            <td colspan="2">Also includes Jar and Zip files when searching for DEX files under the provided classpath.
            </td>
        </tr>
        <tr>
            <td><tt>-process-path <var>dir</var></tt><br><tt>-process-dir <var>dir</var></tt><br></td>
            <td colspan="2">Process all classes found in
               <var>dir</var>
            </td>
        </tr>
        <tr>
            <td><tt>-oaat </tt><br></td>
            <td colspan="2">From the process-dir, processes one class at a time.</td>
        </tr>
        <tr>
            <td><tt>-android-jars <var>path</var></tt><br></td>
            <td colspan="2">Use
               <var>path</var>
               as the path for finding the android.jar file
            </td>
        </tr>
        <tr>
            <td><tt>-force-android-jar <var>path</var></tt><br></td>
            <td colspan="2">Force Soot to use
               <var>path</var>
               as the path for the android.jar file.
            </td>
        </tr>
        <tr>
            <td><tt>-android-api-version <var>version</var></tt><br></td>
            <td colspan="2">Force Soot to use
               <var>version</var>
               as the API version when readin in APK or DEX files.
            </td>
        </tr>
        <tr>
            <td><tt>-ast-metrics </tt><br></td>
            <td colspan="2">Compute AST Metrics if performing java to jimple</td>
        </tr>
        <tr>
            <td><tt>-src-prec <var>format</var></tt><br></td>
            <td><tt>c&nbsp;
                  </tt><tt>class&nbsp;
                  </tt><br><tt>only-class&nbsp;
                  </tt><br><tt>J&nbsp;
                  </tt><tt>jimple&nbsp;
                  </tt><br><tt>java&nbsp;
                  </tt><br><tt>apk&nbsp;
                  </tt><br><tt>apk-class-jimple&nbsp;
                  </tt><tt>apk-c-j&nbsp;
                  </tt><br></td>
            <td colspan="1">Sets source precedence to
               <var>format</var>
               files
            </td>
        </tr>
        <tr>
            <td><tt>-full-resolver </tt><br></td>
            <td colspan="2">Force transitive resolving of referenced classes</td>
        </tr>
        <tr>
            <td><tt>-allow-phantom-refs </tt><br></td>
            <td colspan="2">Allow unresolved classes; may cause errors</td>
        </tr>
        <tr>
            <td><tt>-allow-phantom-elms </tt><br></td>
            <td colspan="2">Allow phantom methods and fields in non-phantom classes</td>
        </tr>
        <tr>
            <td><tt>-no-bodies-for-excluded </tt><br></td>
            <td colspan="2">Do not load bodies for excluded classes</td>
        </tr>
        <tr>
            <td><tt>-j2me </tt><br></td>
            <td colspan="2">Use J2ME mode; changes assignment of types</td>
        </tr>
        <tr>
            <td><tt>-main-class <var>class</var></tt><br></td>
            <td colspan="2">Sets the main class for whole-program analysis.</td>
        </tr>
        <tr>
            <td><tt>-polyglot </tt><br></td>
            <td colspan="2">Use Java 1.4 Polyglot frontend instead of JastAdd</td>
        </tr>
        <tr>
            <td><tt>-permissive-resolving </tt><br></td>
            <td colspan="2">Use alternative sources when classes cannot be found using the normal resolving strategy
            </td>
        </tr>
        <tr>
            <td><tt>-drop-bodies-after-load </tt><br></td>
            <td colspan="2">Drop the method source after it has served its purpose of loading the method body</td>
        </tr>
    </tbody>
</table>

#### Output

<table>
    <tbody>
        <tr>
            <td><tt>-d <var>dir</var></tt><br><tt>-output-dir <var>dir</var></tt><br></td>
            <td colspan="2">Store output files in
               <var>dir</var>
            </td>
        </tr>
        <tr>
            <td><tt>-f <var>format</var></tt><br><tt>-output-format <var>format</var></tt><br></td>
            <td><tt>J&nbsp;
                  </tt><tt>jimple&nbsp;
                  </tt><br><tt>j&nbsp;
                  </tt><tt>jimp&nbsp;
                  </tt><br><tt>S&nbsp;
                  </tt><tt>shimple&nbsp;
                  </tt><br><tt>s&nbsp;
                  </tt><tt>shimp&nbsp;
                  </tt><br><tt>B&nbsp;
                  </tt><tt>baf&nbsp;
                  </tt><br><tt>b&nbsp;
                  </tt><br><tt>G&nbsp;
                  </tt><tt>grimple&nbsp;
                  </tt><br><tt>g&nbsp;
                  </tt><tt>grimp&nbsp;
                  </tt><br><tt>X&nbsp;
                  </tt><tt>xml&nbsp;
                  </tt><br><tt>dex&nbsp;
                  </tt><br><tt>force-dex&nbsp;
                  </tt><br><tt>n&nbsp;
                  </tt><tt>none&nbsp;
                  </tt><br><tt>jasmin&nbsp;
                  </tt><br><tt>c&nbsp;
                  </tt><tt>class&nbsp;
                  </tt><br><tt>d&nbsp;
                  </tt><tt>dava&nbsp;
                  </tt><br><tt>t&nbsp;
                  </tt><tt>template&nbsp;
                  </tt><br><tt>a&nbsp;
                  </tt><tt>asm&nbsp;
                  </tt><br></td>
            <td colspan="1">Set output format for Soot</td>
        </tr>
        <tr>
            <td><tt>-java-version <var>version</var></tt><br></td>
            <td><tt>default&nbsp;
                  </tt><br><tt>1.1&nbsp;
                  </tt><tt>1&nbsp;
                  </tt><br><tt>1.2&nbsp;
                  </tt><tt>2&nbsp;
                  </tt><br><tt>1.3&nbsp;
                  </tt><tt>3&nbsp;
                  </tt><br><tt>1.4&nbsp;
                  </tt><tt>4&nbsp;
                  </tt><br><tt>1.5&nbsp;
                  </tt><tt>5&nbsp;
                  </tt><br><tt>1.6&nbsp;
                  </tt><tt>6&nbsp;
                  </tt><br><tt>1.7&nbsp;
                  </tt><tt>7&nbsp;
                  </tt><br><tt>1.8&nbsp;
                  </tt><tt>8&nbsp;
                  </tt><br><tt>1.9&nbsp;
                  </tt><tt>9&nbsp;
                  </tt><br></td>
            <td colspan="1">Force Java version of bytecode generated by Soot.</td>
        </tr>
        <tr>
            <td><tt>-outjar </tt><br><tt>-output-jar </tt><br></td>
            <td colspan="2">Make output dir a Jar file instead of dir</td>
        </tr>
        <tr>
            <td><tt>-hierarchy-dirs </tt><br></td>
            <td colspan="2">Generate class hierarchy directories for Jimple/Shimple</td>
        </tr>
        <tr>
            <td><tt>-xml-attributes </tt><br></td>
            <td colspan="2">Save tags to XML attributes for Eclipse</td>
        </tr>
        <tr>
            <td><tt>-print-tags </tt><br><tt>-print-tags-in-output </tt><br></td>
            <td colspan="2">Print tags in output files after stmt</td>
        </tr>
        <tr>
            <td><tt>-no-output-source-file-attribute </tt><br></td>
            <td colspan="2">Don't output Source File Attribute when producing class files</td>
        </tr>
        <tr>
            <td><tt>-no-output-inner-classes-attribute </tt><br></td>
            <td colspan="2">Don't output inner classes attribute in class files</td>
        </tr>
        <tr>
            <td><tt>-dump-body <var>phaseName</var></tt><br></td>
            <td colspan="2">Dump the internal representation of each method before and after phase
               <var>phaseName</var>
            </td>
        </tr>
        <tr>
            <td><tt>-dump-cfg <var>phaseName</var></tt><br></td>
            <td colspan="2">Dump the internal representation of each CFG constructed during phase
               <var>phaseName</var>
            </td>
        </tr>
        <tr>
            <td><tt>-show-exception-dests </tt><br></td>
            <td colspan="2">Include exception destination edges as well as CFG edges in dumped CFGs</td>
        </tr>
        <tr>
            <td><tt>-gzip </tt><br></td>
            <td colspan="2">GZip IR output files</td>
        </tr>
        <tr>
            <td><tt>-force-overwrite </tt><br></td>
            <td colspan="2">Force Overwrite Output Files</td>
        </tr>
    </tbody>
</table>

#### Processing
<table>
    <tbody>
        <tr>
            <td><tt>-plugin <var>file</var></tt><br></td>
            <td colspan="2">Load all plugins found in
               <var>file</var>
            </td>
        </tr>
        <tr>
            <td><tt>-wrong-staticness <var>arg</var></tt><br></td>
            <td><tt>fail&nbsp;
                  </tt><br><tt>ignore&nbsp;
                  </tt><br><tt>fix&nbsp;
                  </tt><br><tt>fixstrict&nbsp;
                  </tt><br></td>
            <td colspan="1">Ignores or fixes errors due to wrong staticness</td>
        </tr>
        <tr>
            <td><tt>-field-type-mismatches <var>arg</var></tt><br></td>
            <td><tt>fail&nbsp;
                  </tt><br><tt>ignore&nbsp;
                  </tt><br><tt>null&nbsp;
                  </tt><br></td>
            <td colspan="1">Specifies how errors shall be handled when resolving field references with mismatching
               types
            </td>
        </tr>
        <tr>
            <td><tt>-p <var>phase opt:val</var></tt><br><tt>-phase-option <var>phase opt:val</var></tt><br></td>
            <td colspan="2">Set <var>phase</var>'s <var>opt</var> option to
               <var>value</var>
            </td>
        </tr>
        <tr>
            <td><tt>-O </tt><br><tt>-optimize </tt><br></td>
            <td colspan="2">Perform intraprocedural optimizations</td>
        </tr>
        <tr>
            <td><tt>-W </tt><br><tt>-whole-optimize </tt><br></td>
            <td colspan="2">Perform whole program optimizations</td>
        </tr>
        <tr>
            <td><tt>-via-grimp </tt><br></td>
            <td colspan="2">Convert to bytecode via Grimp instead of via Baf</td>
        </tr>
        <tr>
            <td><tt>-via-shimple </tt><br></td>
            <td colspan="2">Enable Shimple SSA representation</td>
        </tr>
        <tr>
            <td><tt>-throw-analysis <var>arg</var></tt><br></td>
            <td><tt>pedantic&nbsp;
                  </tt><br><tt>unit&nbsp;
                  </tt><br><tt>dalvik&nbsp;
                  </tt><br></td>
            <td colspan="1"></td>
        </tr>
        <tr>
            <td><tt>-check-init-ta <var>arg</var></tt><br><tt>-check-init-throw-analysis <var>arg</var></tt><br></td>
            <td><tt>auto&nbsp;
                  </tt><br><tt>pedantic&nbsp;
                  </tt><br><tt>unit&nbsp;
                  </tt><br><tt>dalvik&nbsp;
                  </tt><br></td>
            <td colspan="1"></td>
        </tr>
        <tr>
            <td><tt>-omit-excepting-unit-edges </tt><br></td>
            <td colspan="2">Omit CFG edges to handlers from excepting units which lack side effects</td>
        </tr>
        <tr>
            <td><tt>-trim-cfgs </tt><br></td>
            <td colspan="2">Trim unrealizable exceptional edges from CFGs</td>
        </tr>
        <tr>
            <td><tt>-ire </tt><br><tt>-ignore-resolution-errors </tt><br></td>
            <td colspan="2">Does not throw an exception when a program references an undeclared field or method.
            </td>
        </tr>
    </tbody>
</table>

### Use Cases

#### Control flow graph construction

You can access the callgraph constructed by Soot through calling:
```java
Callgraph cg = Scene.v().getCallGraph();
```

Then, it is possible to iterate the edges in the cg, e.g.:
```java
SootMethod m = b.getMethod();
Iterator edgeIt = cg.edgesOutOf(m);
```

Soot provides several different control flow graphs (CFG) in the package
soot.toolkits.graph. 

At the base of these graphs sits the interface DirectedGraph;
it defines methods for getting: the entry and exit points to the graph, the successors and predecessors of a given node, an iterator to iterate over the graph
in some undefined order and the graphs size (number of nodes).

The implementations we will describe here are those that represent a CFG
in which the nodes are Soot Units. 
The base class for these kinds of graphs is UnitGraph, an abstract class that
provides facilities to build CFGs. 
There are three different implementations of
it: BriefUnitGraph, ExceptionalUnitGraph and TrapUnitGraph.
* BriefUnitGraph is very simple in the sense that it doesn’t have edges representing control flow due to exceptions being thrown.
* ExceptionalUnitGraph includes edges from throw clauses to their handler
(catch block, referred to in Soot as Trap), that is if the trap is local
to the method body. Additionally, this graph takes into account exceptions that might be implicitly thrown by the VM (e.g. ArrayIndexOutOfBoundsException). For every unit that might throw an implicit exception, there will be an edge from each of that units predecessors to the
respective trap handler’s first unit. Furthermore, should the excepting
unit contain side effects an edge will also be added from it to the trap
handler. If it has no side effects this edge can be selectively added or not
26
with a parameter passed to one of the graphs constructors. This is the
CFG generally used when performing control flow analyses.
* TrapUnitGraph like ExceptionalUnitGraph, takes into account exceptions
that might be thrown. There are three major differences:
1. Edges are added from every trapped unit (i.e., within a try block)
to the trap handler.
2. There are no edges from predecessors of units that may throw an
implicit exception to the trap handler (unless they are also trapped).
3. There is always an edge from a unit that may throw an implicit
exception to the trap handler.

To build a CFG for a given method body you simply pass the body to one
of the CFG constructors — e.g.:
```java
UnitGraph g = new ExceptionalUnitGraph(body);
```

#### Point-to Analysis

#### Reverse engineer apps

#### Instrument apps

**TODO** 