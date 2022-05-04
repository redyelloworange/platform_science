# Function

Calculates the suitability score under the specification provided in "SDE
Coding Challenge" from Platform Science.  

# Dependencies

* Python 3.9
* Optional: Virtual environment
* `pip install -r requirements.txt`

# Usage

`python3.9 main.py --driver-file DRIVER_FILE --shipment-destination-file 
SHIPMENT_DESTINATION_FILE`

Provide the `-h` flag when running `main.py` for additional details.

# Sample output

    Bo Darville, 4 Privet Drive
    Cledus Snow, 742 Evergreen Terrace
    Homer Simpson, 17 Cherry Tree Lane
    Red Barclay, 221B Baker Street
    ========================================
    Total suitability score: 43.5

# Approach

Create each possible permutation of driver and destination, memoizing 
calculations for future reference.  This does have a risk of taking up an 
excess of memory.  It would be reasonable to use a least-recently-used 
cache or something like that in order to get a better compromise.