@ECHO OFF
CHCP 65001
set var=3
:continue
D:\soft\Python35\Scripts\you-get.exe --debug "http://www.icourses.cn/jpk/changeforVideo.action?resId=540262&courseId=7001&firstShowFlag=42"
if exist *.flv Pause Break
if %var% gtr 0 goto continue

