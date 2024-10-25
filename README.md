# vcard-to-csv
<h1>vCard to CSV Converter
<h2></h2>Overview
The vCard to CSV Converter is a practical tool designed to transform vCard files—commonly used by Gmail—into a CSV format compatible with Microsoft Outlook. This conversion facilitates the seamless import of contacts into Outlook, accommodating the specific data mapping requirements of the application.

<h2>Supported Fields
The following fields are currently supported during the conversion process:

FN: Full Name
ORG: Organization
EMAIL: Email Address
TEL: Telephone Number
ADR: Address
BDAY: Birthday
Customization
Please note that not all fields may be automatically converted. If you require additional fields, you may need to modify the code to include them according to your needs.

<h2>Usage Instructions
To utilize the converter, you need to provide two parameters:

vCard File: The path to the vCard file you wish to convert.
Output File: The desired name and location for the transformed CSV file.
Example Function Call

convert_vcard_to_csv('path/to/vcard.vcf', 'path/to/output.csv')

<h2>Remapping Fields in Outlook
After importing the CSV file into Outlook, you may need to remap individual input fields to ensure everything functions correctly. Keep in mind that the auto-complete feature in Outlook might not include all fields unless explicitly configured.

<h2>Special Considerations for Character Encoding
If you are working with languages that contain special characters such as ä, ö, and ü, it is advisable to replace these characters with their ASCII equivalents (e.g., ä → ae, ö → oe, ü → ue). This adjustment is necessary because Outlook may not handle these special characters correctly during the import process.

<h2>Conclusion
The vCard to CSV Converter simplifies the migration of contact information from Gmail to Outlook, ensuring that your contacts are correctly formatted and ready for use. For any issues or suggestions, please feel free to raise an issue or submit a pull request on this repository.
