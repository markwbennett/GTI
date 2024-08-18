This folder contains files for tuning a 2015 GTI.

The tune uses:

* Simostools to interface between Android and VW ECU, upload tunes, and log data. (https://play.google.com/store/apps/details?id=com.app.simostools)
* A homebuilt Macchina A0 clone to connect the Android to the ECU.
* TunerPro to change parameters in the tune. (https://tunerpro.net)
* MegaLogViewer HD to analyze data logged by Simostools. (https://www.efianalytics.com/MegaLogViewerHD/)
* Google Drive to move data between computer and Android (e.g. edit the tune on the desktop, save it to the Google Drive, install it from the Drive to the car using the Android).

Files are:

BINs, which are the binary files uploaded to the ECU,
XDFs, which are the xml definition files that TunerPro uses to map locations in the ECU's memory to human-readable and editable fields.
A2Ls, which are the xml files that describe all of the locations in the ECU's memory.
Logs, which are the CSV log files that Simostools records,
PID lists, which are the csv files that tell SimosTools what parameters to log, and what they mean.
