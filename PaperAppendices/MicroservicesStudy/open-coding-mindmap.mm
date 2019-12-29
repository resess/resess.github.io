<map version="1.0.1">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1543608657945" ID="ID_1825957001" MODIFIED="1576890141120" STYLE="bubble" TEXT="Study">
<edge COLOR="#808080" STYLE="bezier" WIDTH="thin"/>
<node CREATED="1543608678622" ID="ID_1147878348" MODIFIED="1550689702363" POSITION="right" STYLE="bubble">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Architecture
    </p>
  </body>
</html></richcontent>
<edge COLOR="#808080" STYLE="bezier" WIDTH="thin"/>
<node CREATED="1543609389734" ID="ID_1926501481" MODIFIED="1552030183809">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Microservice
    </p>
    <p>
      granularity
    </p>
  </body>
</html></richcontent>
<node CREATED="1543609402795" ID="ID_609775231" MODIFIED="1552030184155" TEXT="Split by business capabilities">
<node CREATED="1543609404494" ID="ID_1742506137" MODIFIED="1543609405847" TEXT="16"/>
</node>
<node CREATED="1543609409775" ID="ID_1412219918" MODIFIED="1552030184156" TEXT="Split by data access">
<node CREATED="1543609412802" ID="ID_463818264" MODIFIED="1543609416026" TEXT="6"/>
</node>
<node CREATED="1543609423191" ID="ID_751696263" MODIFIED="1552030184156" TEXT="Split by team structure">
<node CREATED="1543609424379" ID="ID_1629549322" MODIFIED="1543609425100" TEXT="3"/>
</node>
<node CREATED="1543609430203" ID="ID_511758295" MODIFIED="1552030184157" TEXT="Split by dependencies">
<node CREATED="1543609431209" ID="ID_1490665901" MODIFIED="1552032021523" TEXT="5"/>
</node>
<node CREATED="1576888863326" ID="ID_1090166128" MODIFIED="1576889222392" TEXT="Split by delivery cycles">
<icon BUILTIN="stop-sign"/>
<node CREATED="1576889303265" ID="ID_20954018" MODIFIED="1576889744287" TEXT="1 interviewee">
<icon BUILTIN="stop-sign"/>
</node>
</node>
<node CREATED="1543609436858" ID="ID_1637493641" MODIFIED="1576888897111" TEXT="Split by resource consumption">
<node CREATED="1543609442462" ID="ID_543469983" MODIFIED="1552032023524" TEXT="10"/>
</node>
</node>
<node CREATED="1543608932250" ID="ID_1926981922" MODIFIED="1576889064343">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Microservice
    </p>
    <p>
      ownership
    </p>
  </body>
</html></richcontent>
<node CREATED="1543608940011" ID="ID_620452527" MODIFIED="1552030184161" TEXT="Fixing defects is the responsibility of service owners">
<node CREATED="1543609040365" ID="ID_261880385" MODIFIED="1543609095566" TEXT="6"/>
</node>
<node CREATED="1543609029159" FOLDED="true" ID="ID_1441772067" MODIFIED="1576889112061" TEXT="Architecture decisions are the responsibility of service owners">
<node CREATED="1543609046227" ID="ID_1020505340" MODIFIED="1543609093410" TEXT="7"/>
</node>
<node CREATED="1543609033874" ID="ID_505513173" MODIFIED="1552030184163" TEXT="No owner means no one is responsible">
<node CREATED="1543609048528" ID="ID_1091194490" MODIFIED="1543609100988" TEXT="4"/>
</node>
<node CREATED="1576889071457" ID="ID_108398428" MODIFIED="1576889096343" TEXT="Training newcomers is the responsibility of service owners">
<icon BUILTIN="bookmark"/>
<node CREATED="1576889277615" ID="ID_1436814105" MODIFIED="1576889296534" TEXT="1 survey participant">
<icon BUILTIN="bookmark"/>
</node>
</node>
</node>
<node CREATED="1543609351524" ID="ID_184682340" MODIFIED="1576888752681">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Restricting
    </p>
    <p>
      language
    </p>
    <p>
      diversity
    </p>
  </body>
</html></richcontent>
<node CREATED="1543609364062" ID="ID_1145391617" MODIFIED="1552030184159" TEXT="Using multiple languages hinders understandability">
<node CREATED="1543609366198" ID="ID_9688977" MODIFIED="1543609366915" TEXT="4"/>
</node>
<node CREATED="1543609370497" ID="ID_1354770831" MODIFIED="1576888921529" TEXT="Using multiple languages hinders maintainability">
<node CREATED="1543609372355" ID="ID_1610193108" MODIFIED="1543609373061" TEXT="5"/>
</node>
<node CREATED="1543609377707" ID="ID_732334504" MODIFIED="1576888927658" TEXT="Restrict languages used ( /justify langauges chosen)">
<node CREATED="1543609380771" ID="ID_448436452" MODIFIED="1543609382342" TEXT="6"/>
</node>
</node>
</node>
<node CREATED="1543608669886" ID="ID_1007597884" MODIFIED="1549085815726" POSITION="right" STYLE="bubble" TEXT="Infrastructure">
<edge COLOR="#808080" STYLE="bezier" WIDTH="thin"/>
<node CREATED="1543609227402" ID="ID_1588940115" MODIFIED="1552030183796">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Logging and
    </p>
    <p>
      monitoring
    </p>
  </body>
</html></richcontent>
<node CREATED="1543609233424" ID="ID_1756617401" MODIFIED="1552030184147" TEXT="Logging and monitoring is critical and shouldn&apos;t be an afterthought ">
<node CREATED="1543609236113" ID="ID_730509152" MODIFIED="1549089363476" TEXT="9"/>
</node>
<node CREATED="1543609241529" ID="ID_683497532" MODIFIED="1552030184148" TEXT="Automated anomaly detection in logs">
<node CREATED="1543609243453" ID="ID_1625908999" MODIFIED="1549089384953" TEXT="8"/>
</node>
<node CREATED="1543609250147" ID="ID_1879060522" MODIFIED="1552030184149" TEXT="Log extensive information about services">
<node CREATED="1543609251506" ID="ID_734795988" MODIFIED="1543609252256" TEXT="3"/>
</node>
<node CREATED="1576889144367" ID="ID_133390243" MODIFIED="1576889188774" TEXT="Can be used to create compliance and auditing reports">
<icon BUILTIN="bookmark"/>
<node CREATED="1576889250211" ID="ID_1540317159" MODIFIED="1576889269056" TEXT="1 survey participant">
<icon BUILTIN="bookmark"/>
</node>
</node>
</node>
<node CREATED="1543609264500" ID="ID_1486179780" MODIFIED="1552030183800">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Distributed
    </p>
    <p>
      tracing
    </p>
  </body>
</html></richcontent>
<node CREATED="1543609277614" ID="ID_131487469" MODIFIED="1552030184150" TEXT="Distributed tracing is important and shouldn&apos;t be an afterthought">
<node CREATED="1543609279436" ID="ID_989748185" MODIFIED="1543609281271" TEXT="6"/>
</node>
<node CREATED="1543609285277" ID="ID_1034610889" MODIFIED="1552030184151" TEXT="Tracing requests across microservices is difficult">
<node CREATED="1543609286892" ID="ID_426375504" MODIFIED="1543609288002" TEXT="4"/>
</node>
</node>
<node CREATED="1543609293457" ID="ID_154296604" MODIFIED="1552030183801">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Automating
    </p>
    <p>
      processes
    </p>
  </body>
</html></richcontent>
<node CREATED="1543609298642" ID="ID_1410897970" MODIFIED="1552030184152" TEXT="Automated setup helps reduce cost">
<node CREATED="1543609300535" ID="ID_1500495732" MODIFIED="1543609301321" TEXT="8"/>
</node>
</node>
<node CREATED="1543609314787" ID="ID_1828737127" MODIFIED="1552030183804">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Tools
    </p>
  </body>
</html></richcontent>
<node CREATED="1543609319152" ID="ID_1316815031" MODIFIED="1552030184153" TEXT="Transitioning between tools is unavoidable but costly">
<node CREATED="1543609321107" ID="ID_1333245052" MODIFIED="1543609321812" TEXT="5"/>
</node>
<node CREATED="1543609325866" ID="ID_1107611874" MODIFIED="1552030184154" TEXT="Early adopters had to develop their own tools">
<node CREATED="1543609328737" ID="ID_738618084" MODIFIED="1543609329710" TEXT="7"/>
</node>
</node>
</node>
<node CREATED="1543608686590" ID="ID_459721170" MODIFIED="1549086777297" POSITION="right" STYLE="bubble">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Code
    </p>
    <p>
      Management
    </p>
  </body>
</html></richcontent>
<edge COLOR="#808080" STYLE="bezier" WIDTH="thin"/>
<node CREATED="1543609501466" ID="ID_334101475" MODIFIED="1576888947106">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Common
    </p>
    <p>
      code
    </p>
  </body>
</html></richcontent>
<node CREATED="1543609509129" ID="ID_1852751071" MODIFIED="1552030184163" TEXT="Latest-version shared library">
<node CREATED="1543609512274" ID="ID_882374598" MODIFIED="1543609513123" TEXT="8"/>
</node>
<node CREATED="1543609517170" ID="ID_528337443" MODIFIED="1552030184164" TEXT="Multiple-version shared library">
<node CREATED="1543609521172" ID="ID_145416920" MODIFIED="1563402640846" TEXT="5"/>
</node>
<node CREATED="1543609527913" ID="ID_1486504017" MODIFIED="1552030184164" TEXT="Standalone microservice">
<node CREATED="1543609529889" ID="ID_443243658" MODIFIED="1543609531716" TEXT="5"/>
</node>
<node CREATED="1576888984140" ID="ID_1260583252" MODIFIED="1576889227759" TEXT="Sidecar">
<icon BUILTIN="stop-sign"/>
<node CREATED="1576889746181" ID="ID_1543066145" MODIFIED="1576889812438" TEXT="1 interviewee">
<icon BUILTIN="stop-sign"/>
</node>
</node>
</node>
<node CREATED="1543609452089" ID="ID_1198762909" MODIFIED="1552032068970">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Managing
    </p>
    <p>
      APIs
    </p>
  </body>
</html></richcontent>
<node CREATED="1543609461243" ID="ID_442289322" MODIFIED="1552030184165" TEXT="Direct API calls">
<node CREATED="1543609463989" ID="ID_426628938" MODIFIED="1552032057237" TEXT="15"/>
</node>
<node CREATED="1543609475623" ID="ID_1431775644" MODIFIED="1552030184166" TEXT="Proxy">
<node CREATED="1543609483849" ID="ID_727793133" MODIFIED="1552032063155" TEXT="12"/>
</node>
<node CREATED="1543609490259" ID="ID_341986659" MODIFIED="1552030184166" TEXT="Client library">
<node CREATED="1543609493432" ID="ID_92773917" MODIFIED="1552032065914" TEXT="6"/>
</node>
<node CREATED="1552032068972" ID="ID_1591353654" MODIFIED="1563402661997" TEXT="Message-based communication (e.g., via Message Broker)">
<node CREATED="1552032079682" ID="ID_1680865201" MODIFIED="1552032081988" TEXT="6"/>
</node>
<node CREATED="1543609120712" ID="ID_807000707" MODIFIED="1576889019648" TEXT="Version up APIs when making breaking changes">
<node CREATED="1543609173889" ID="ID_34965738" MODIFIED="1543609174486" TEXT="6"/>
</node>
<node CREATED="1543609155222" ID="ID_1720259795" MODIFIED="1552032104619" TEXT="Interlock calls when making breaking API changes">
<node CREATED="1543609179067" ID="ID_1652708712" MODIFIED="1552032109923" TEXT="5"/>
</node>
<node CREATED="1543609161090" ID="ID_1409503824" MODIFIED="1552030184168" TEXT="Minimize breaking API changes">
<node CREATED="1543609184493" ID="ID_50321283" MODIFIED="1543609185094" TEXT="12"/>
</node>
<node CREATED="1543609165560" ID="ID_106080849" MODIFIED="1576889023271" TEXT="Deprecate old versions to introduce breaking API changes">
<node CREATED="1543609189158" ID="ID_1981247705" MODIFIED="1543609189695" TEXT="8"/>
</node>
</node>
<node CREATED="1543609539185" ID="ID_313985113" MODIFIED="1552030183825">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Managing
    </p>
    <p>
      variants
    </p>
  </body>
</html></richcontent>
<node CREATED="1543609544871" ID="ID_1839861378" MODIFIED="1552030184170" TEXT="Feature flags">
<node CREATED="1543609546045" ID="ID_1370268891" MODIFIED="1543609547406" TEXT="10"/>
</node>
<node CREATED="1543609551392" ID="ID_1653304290" MODIFIED="1563402406535" TEXT="Role-based access">
<node CREATED="1543609553152" ID="ID_602746442" MODIFIED="1543609554188" TEXT="7"/>
</node>
<node CREATED="1543609557775" ID="ID_1042370641" MODIFIED="1563402407236" TEXT="Separate deployments">
<node CREATED="1543609558926" ID="ID_1414205542" MODIFIED="1549090003772" TEXT="8"/>
</node>
</node>
</node>
</node>
</map>
