# RTLS Locators Calculator

A Windows desktop application for estimating the number of RTLS locators needed in a rectangular room. It provides a simple Tkinter interface for entering room dimensions and installation heights.

## Features

- Calculates the room area from length and width.
- Estimates locators for 0.3-meter and 3-meter accuracy configurations.
- Uses the locator-to-tag height difference in the coverage calculation.
- Displays warnings for invalid heights, minimum locator requirements, and unreliable tag-height scenarios.
- Includes reset and input validation controls.

## Requirements

- Python 3
- Tkinter (included with the standard Windows Python installation)

No third-party Python packages are required.

## Run the application

From the project directory, run:

```powershell
python .\Locator.py
```

## How to use

1. Enter the room **Length L** in meters.
2. Enter the room **Width W** in meters.
3. Enter the **Locator Height** in meters.
4. Enter the **Tag Height** in meters.
5. Select **Calculate**.

The application displays:

- **Total Room Area**: room length multiplied by room width.
- **0.3 meters Accuracy Locators**: estimated locator count rounded up.
- **3 meters Accuracy Locators**: estimated locator count rounded up.

## Calculation rules

- The locator height must not exceed 10 meters.
- The locator must be installed above the tag.
- The minimum recommended locator count is 2.
- The result is marked unavailable when the tag height exceeds 67% of the locator height.
- A reliability warning is shown when the tag height exceeds 52% of the locator height.

## Example

For a room measuring 20 meters by 10 meters, with a locator height of 5 meters and a tag height of 1 meter:

- Room area: `200 m²`
- Height difference: `4 m`
- The estimated locator counts are shown in the result panel.

## Reset

Select **Reset** to clear all input fields and results.