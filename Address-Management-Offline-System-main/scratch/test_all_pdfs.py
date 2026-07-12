import sys
import os
sys.path.append(os.path.abspath('.'))
from modules.print_module import (
    generate_address_list_pdf,
    generate_department_list_pdf,
    generate_reference_labels_pdf,
    generate_single_label_pdf,
    generate_full_directory_pdf
)

dummy_records = [
    {
        "to_field": "Director",
        "designation": "Scientist",
        "office_name": "ADRDE",
        "addr_line1": "Station Road",
        "addr_line2": "Agra Cantt",
        "city": "Agra",
        "state": "UP",
        "pin_code": "282001",
        "para_no": "PARA/123",
        "date_entry": "2026-07-12",
        "delivery_type": "Ordinary/???????",
        "dept_name": "IT Dept",
        "email": "test@drdo.com",
        "contact_no": "1234567890",
        "fax": "0987654321"
    }
] * 3

print("Testing generate_address_list_pdf...")
res, msg = generate_address_list_pdf(dummy_records, "scratch/test_address_list.pdf")
print(res, msg)

print("Testing generate_department_list_pdf...")
res, msg = generate_department_list_pdf(dummy_records, "IT Dept", "scratch/test_dept_list.pdf")
print(res, msg)

print("Testing generate_reference_labels_pdf...")
res, msg = generate_reference_labels_pdf(dummy_records, "scratch/test_ref_labels.pdf")
print(res, msg)

print("Testing generate_single_label_pdf...")
res, msg = generate_single_label_pdf(dummy_records[0], "scratch/test_single_label.pdf")
print(res, msg)

print("Testing generate_full_directory_pdf...")
res, msg = generate_full_directory_pdf(dummy_records, "scratch/test_full_dir.pdf")
print(res, msg)

print("All tests completed.")
