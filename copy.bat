@echo off
setlocal enabledelayedexpansion
set /A Counter=1
pushd G:\DANTE\parcial2
for /r %%a in (*.apk) do (
  COPY "%%a" "G:\DANTE\mutantes\com.evancharlton.mileage.mutante.!Counter!.apk"
  set /A Counter+=1
)
popd