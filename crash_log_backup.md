## Crash Details

**Crash Thread**: `Thread[main,5,main]`  
**Crash Timestamp**: `2026-07-01 20:18:19.453 UTC`  

**Crash Message**:
```
android.os.DeadSystemException
```


### Stacktrace

```
android.os.DeadSystemRuntimeException: android.os.DeadSystemException
	at android.app.ActivityClient.activityResumed(ActivityClient.java:68)
	at android.app.servertransaction.ResumeActivityItem.postExecute(ResumeActivityItem.java:82)
	at android.app.servertransaction.TransactionExecutor.executeLifecycleItem(TransactionExecutor.java:185)
	at android.app.servertransaction.TransactionExecutor.executeTransactionItems(TransactionExecutor.java:116)
	at android.app.servertransaction.TransactionExecutor.execute(TransactionExecutor.java:89)
	at android.app.ActivityThread$H.handleMessage(ActivityThread.java:3553)
	at android.os.Handler.dispatchMessage(Handler.java:124)
	at android.os.Looper.loopOnce(Looper.java:263)
	at android.os.Looper.loop(Looper.java:360)
	at android.app.ActivityThread.main(ActivityThread.java:10806)
	at java.lang.reflect.Method.invoke(Native Method)
	at com.android.internal.os.RuntimeInit$MethodAndArgsCaller.run(RuntimeInit.java:648)
	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:1012)
Caused by: android.os.DeadSystemException
	... 13 more

```
##


## Termux App Info

**APP_NAME**: `Termux`  
**PACKAGE_NAME**: `com.termux`  
**VERSION_NAME**: `0.118.3`  
**VERSION_CODE**: `1002`  
**TARGET_SDK**: `28`  
**IS_DEBUGGABLE_BUILD**: `false`  
**SE_PROCESS_CONTEXT**: `u:r:untrusted_app_27:s0:c227,c256,c512,c768`  
**SE_FILE_CONTEXT**: `u:object_r:app_data_file:s0:c227,c256,c512,c768`  
**SE_INFO**: `default:targetSdkVersion=28:complete`  
**APK_RELEASE**: `F-Droid`  
**SIGNING_CERTIFICATE_SHA256_DIGEST**: `228FB2CFE90831C1499EC3CCAF61E96E8E1CE70766B9474672CE427334D41C42`  
##


## Device Info

### Software

**OS_VERSION**: `6.1.138-android14-11-g0c3d559bcd85-ab14529422`  
**SDK_INT**: `36`  
**RELEASE**: `16`  
**ID**: `HONORLGN-N31S`  
**DISPLAY**: `LGN-N31S 10.0.0.142(C430E7R2P1)`  
**INCREMENTAL**: `10.0.0.142C430E7R2P1`  
**SECURITY_PATCH**: `2026-05-01`  
**IS_TREBLE_ENABLED**: `true`  
**TYPE**: `user`  
**TAGS**: `release-keys`  

### Hardware

**MANUFACTURER**: `HONOR`  
**BRAND**: `HONOR`  
**MODEL**: `LGN-NX1`  
**PRODUCT**: `LGN-NX1EEA`  
**BOARD**: `blair`  
**HARDWARE**: `qcom`  
**DEVICE**: `HNLGN-Q1`  
**SUPPORTED_ABIS**: `arm64-v8a`  
**SUPPORTED_32_BIT_ABIS**:   
**SUPPORTED_64_BIT_ABIS**: `arm64-v8a`  
**PAGE_SIZE**: `4096`  
##
