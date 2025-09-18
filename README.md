# 🚌 transittool

**transittool** is a command-line utility for managing and analyzing Vancouver Translink trip data. It summarizes your bus and skytrain trip records, making it easier to track your public transportation spending.

## Quick Installation For Non-Developers
1. Make sure `~/.local/bin` is in your `$PATH`.
2. Install the `transittool` script.
```bash
curl -o ~/.local/bin/transittool https://raw.githubusercontent.com/carhuang/transittool/refs/heads/main/transittool
chmod +x ~/.local/bin/transittool
```

## Installation For Developers
1. Clone the project.
```bash
git clone https://github.com/carhuang/transittool.git
cd transittool
```
2. Make the script executable.
```bash
chmod +x transittool
```
3. By default, the executable binary will be stored in `~/.local/bin`. You can change this by changing the value of `BINDIR` in the `Makefile`. Make sure `~/.local/bin` (or your custom `BINDIR` location) is in your `$PATH`. 
2. Run `make install` to create a symlink in your binary directory. `transittool` is now ready for system-wide usage.

## Requirements
- Python 3.6+
- A CSV file containing your Translink trip records downloaded from the [Compass Card Website](https://www.compasscard.ca/SignIn). *Do not* rename the downloaded CSV file. The CSV data file names must contain date ranges in the format `MM-DD-YYYY` to `MM-DD-YYYY` because `transittool` uses it to determine the date range of the records. The downloaded raw CSV data file name should look like `Compass Card History - <your compass card number> - May-25-2024 to Jun-19-2025.csv`.

## Usage
#### Initialize a master CSV data file:
After downloading your CSV data file, run the `init` command to initialize a `master.csv` file in `~/.local/share/transittool`. The `master.csv` file will contain cleaned up data from your original dowloaded CSV data file.
```bash
transittool init "Compass Card History - ...csv"
```
This command should only need to be run once, unless you accidentally deleted `master.csv`.
#### Show monthly summary:
```bash
transittool summary
```
#### Show date range of data:
When you want to update your Translink trip record, run the `date` command to see which new trip data you will need to download.
```bash
transittool date
```
#### Append new data:
After downloading new Translink trip record from the [Compass Card Website](https://www.compasscard.ca/SignIn), run the `append` command to append new data to `master.csv`.
```bash
transittool append "Compass Card History - ...csv"
```
#### Show tool manual:
```bash
transittool --help
```

## Testing

## Uninstallation for Non-Developers
```bash
rm -rf ~/.local/bin/transittool
rm -rf ~/.local/share/transittool
```

## Uninstallation for Developers
1. Remove the installed symlink.
```bash
make uninstall
```
2. Delete the project folder and the meta file folder.
```bash
rm -rf /path/to/transittool
rm -rf ~/.local/share/transittool
```