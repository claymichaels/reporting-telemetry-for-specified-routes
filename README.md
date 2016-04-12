# reporting-telemetry-for-specified-routes
A follow-up report to "reporting-derailment-speed", tracking telemetry for certain routes over time.

After the previous report, I got a request to pull the telemetry records for hundreds of train routes, given customer schedule .XLS spreadhseets as input.
This report parses those input files, determines routes that meet the criteria from the customer, and writes telemetry .CSVs for each.
