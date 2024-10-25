import csv

def vcard_to_csv(vcard_file, csv_file):
    # Prepare CSV data
    csv_data = []
    headers = [
        "Anrede", "Vorname", "Weitere Vornamen", "Nachname", "Suffix",
        "Firma", "Abteilung", "Position", "Straße geschäftlich",
        "Straße geschäftlich 2", "Straße geschäftlich 3", "Ort geschäftlich",
        "Region geschäftlich", "Postleitzahl geschäftlich", "Land/Region geschäftlich",
        "Straße privat", "Straße privat 2", "Straße privat 3", "Ort privat",
        "Bundesland/Kanton privat", "Postleitzahl privat", "Land/Region privat",
        "Weitere Straße", "Weitere Straße 2", "Weitere Straße 3",
        "Weiterer Ort", "Weiteres/r Bundesland/Kanton", "Weitere Postleitzahl",
        "Weiteres/e Land/Region", "Telefon Assistent", "Fax geschäftlich",
        "Telefon geschäftlich", "Telefon geschäftlich 2", "Rückmeldung",
        "Autotelefon", "Telefon Firma", "Fax privat", "Telefon (privat)",
        "Telefon (privat 2)", "ISDN", "Mobiltelefon", "Weiteres Fax",
        "Weiteres Telefon", "Pager", "Haupttelefon", "Mobiltelefon 2",
        "Telefon für Hörbehinderte", "Telex", "Abrechnungsinformation",
        "Assistent(in)", "Benutzer 1", "Benutzer 2", "Benutzer 3",
        "Benutzer 4", "Beruf", "Büro", "E-Mail-Adresse", "E-Mail-Typ",
        "E-Mail: Angezeigter Name", "E-Mail 2: Adresse", "E-Mail 2: Typ",
        "E-Mail 2: Angezeigter Name", "E-Mail 3: Adresse", "E-Mail 3: Typ",
        "E-Mail 3: Angezeigter Name", "Empfohlen von", "Geburtstag",
        "Geschlecht", "Hobby", "Initialen", "Internet Frei/Gebucht",
        "Jahrestag", "Kategorien", "Kinder", "Konto", "Name des/r Vorgesetzten",
        "Notizen", "Organisationsnr.", "Ort", "Partner/in",
        "Postfach geschäftlich", "Postfach privat", "Priorität",
        "Privat", "Reisekilometer", "Sozialversicherungsnr.",
        "Sprache", "Stichwörter", "Vertraulichkeit", "Verzeichnisserver",
        "Webseite", "Weiteres Postfach"
    ]
    
    csv_data.append(headers)

    # Read vCard file
    with open(vcard_file, 'r', encoding='utf-8') as vcard:
        contact = {}
        
        for line in vcard:
            line = line.strip()
            if line.startswith("BEGIN:VCARD"):
                contact = {header: "" for header in headers}  # Reset for new contact
            elif line.startswith("FN:"):
                full_name = line[3:].split()
                contact["Vorname"] = full_name[0] if len(full_name) > 0 else ""
                contact["Nachname"] = full_name[-1] if len(full_name) > 1 else ""
            elif line.startswith("ORG:"):
                contact["Firma"] = line[4:]  # Company
            elif line.startswith("EMAIL"):
                # Extract the email and types from the line
                email_parts = line.split(":")
                email = email_parts[1] if len(email_parts) > 1 else ""
                types = [part.replace("type=", "") for part in email_parts[0].split(";") if "type=" in part]
                # Determine the field based on types (e.g., pref, HOME, WORK)
                if "pref" in types or "WORK" in types:
                    if not contact["E-Mail-Adresse"]:
                        contact["E-Mail-Adresse"] = email
                        contact["E-Mail-Typ"] = "SMTP"
                        contact["E-Mail: Angezeigter Name"] = contact.get("FN", "")
                elif "HOME" in types:
                    if not contact["E-Mail 2: Adresse"]:
                        contact["E-Mail 2: Adresse"] = email
                        contact["E-Mail 2: Typ"] = "SMTP"
                else:
                    if not contact["E-Mail 3: Adresse"]:
                        contact["E-Mail 3: Adresse"] = email
                        contact["E-Mail 3: Typ"] = "SMTP" 

            elif line.startswith("TEL"):
                # Extract the phone number and types
                tel_parts = line.split(":")
                phone_number = tel_parts[1].strip() if len(tel_parts) > 1 else ""
                types = [part.replace("type=", "") for part in tel_parts[0].split(";") if "type=" in part]
                
                # Determine the field based on types (e.g., pref, CELL, WORK, FAX, VOICE)
                if "CELL" in types:
                    if not contact["Mobiltelefon"]:
                        contact["Mobiltelefon"] = phone_number
                    elif "pref" in types:
                        contact["Mobiltelefon"] = phone_number  # Replace if marked as preferred
                elif "WORK" in types:
                    if "FAX" in types:
                        contact["Fax geschäftlich"] = phone_number
                    elif not contact["Telefon geschäftlich"]:
                        contact["Telefon geschäftlich"] = phone_number
                    elif "pref" in types:
                        contact["Telefon geschäftlich"] = phone_number  # Replace if marked as preferred
                elif "HOME" in types or "VOICE" in types:
                    if not contact["Telefon (privat)"]:
                        contact["Telefon (privat)"] = phone_number
                    elif "pref" in types:
                        contact["Telefon (privat)"] = phone_number  # Replace if marked as preferred
                elif "FAX" in types and not contact["Weiteres Fax"]:
                    contact["Weiteres Fax"] = phone_number
                else:
                    # General fallback if no specific type is provided
                    if not contact["Haupttelefon"]:
                        contact["Haupttelefon"] = phone_number


            elif line.startswith("ADR;type=WORK:") or line.startswith("ADR;type=WORK;type=pref:"):
                # Extract and split the address components after ":"
                address_parts = line.split(":", 1)[1].split(";")

                # Map the address components for the business address
                contact["Straße geschäftlich"] = address_parts[2] if len(address_parts) > 2 else ""
                contact["Ort geschäftlich"] = address_parts[3] if len(address_parts) > 3 else ""
                contact["Postleitzahl geschäftlich"] = address_parts[5] if len(address_parts) > 5 else ""
                contact["Land/Region geschäftlich"] = address_parts[6] if len(address_parts) > 6 else ""

            elif line.startswith("ADR;type=HOME:") or line.startswith("ADR;type=HOME;type=pref:"):
                # Extract and split the address components after ":"
                address_parts = line.split(":", 1)[1].split(";")

                # Map the address components for the home address
                contact["Straße privat"] = address_parts[2] if len(address_parts) > 2 else ""
                contact["Ort privat"] = address_parts[3] if len(address_parts) > 3 else ""
                contact["Postleitzahl privat"] = address_parts[5] if len(address_parts) > 5 else ""
                contact["Land/Region privat"] = address_parts[6] if len(address_parts) > 6 else ""

            

            elif line.startswith("BDAY:"):
                contact["Geburtstag"] = line[5:]  # Birthday

            elif line.startswith("END:VCARD"):
                csv_data.append(list(contact.values()))  # Add completed contact to CSV data

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        writer.writerows(csv_data)

    print(f"Converted {vcard_file} to {csv_file}")

# Example usage
vcard_to_csv('sets/pythondata.vcard', 'contacts.csv')
