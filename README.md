# Taiwan Invoice Lottery Check

## Summary

Check Taiwan invoice lottery.

## Python 2.7

## Dependencies

- beautifulsoup4

## Windows Binary Build

- Executable file is available [here](https://github.com/marksylee/PythonTools/blob/master/win_exe/invoice_check.zip?raw=true).
- Unzip it and execute **invoice_check.exe**.

## Source Build

- Download and install the latest [Python 2](https://www.python.org/downloads/).
- Install required packages:
  - `pip install -r requirement.txt`
- Double-click the **invoice_check.py** (or use script: `python invoice_check.py`).

## How To Use

- Input your invoice numbers (from right to left).
- The program will check the numbers everytime after you press any key.
- You don't need to input full invoice numbers unless you hit the jackpot.
- When dialogue popup, read it and press Enter (auto reset input and focus).

## Example

Assume your invoice numbers are **12345** and winning numbers are **23456**.
You should press **5** > **4** > **3** > **2** > **1**, but system will alert
you when you input **5**, so you don't need to keyin the rest numbers.

