# import openpyxl
# from datetime import datetime
# from openpyxl.styles import Font, Alignment
# import traceback
# from controllers.logs import Logger
# class Report:
#     def __init__(self, current_date, db_date):
#         # self.current_date = datetime.now().strftime('%m%d%Y')
#         self.current_date = current_date
#         self.db_date = db_date
#         self.output_folder_path = f"output/{self.current_date}/"
#         self.logger = Logger()

#     def create_report(self, db_letter_ids, id_not_found, ids_found, intra_doc_duplicates, cross_doc_duplicates):
#         try:
#             # Create a new Excel workbook
#             wb = openpyxl.Workbook()

#             # Add all sheets
#             self.add_missing_and_found_sheet(wb, db_letter_ids, id_not_found, ids_found)
#             self.add_intra_doc_duplicates_sheet(wb, intra_doc_duplicates)
#             self.add_cross_doc_duplicates_sheet(wb, cross_doc_duplicates)

#             # Save the workbook
#             report_file = f"{self.output_folder_path}{self.current_date}_report.xlsx"
#             wb.save(report_file)
#             print(f"Report saved successfully: {report_file}")
#             return report_file

#         except FileNotFoundError as fe:
#             message = f"Error: The output folder path does not exist: {fe}"
#             self.logger.log_error(message)
#         except PermissionError as pe:
#             message = f"Error: Permission denied while saving the file: {pe}"
#             self.logger.log_error(message)
#         except Exception as e:
#             message = f"Unexpected error in create_report: {e}"
#             self.logger.log_error(message)
#             traceback.print_exc()
#         return None


#     def add_missing_and_found_sheet(self, wb, db_letter_ids, id_not_found, ids_found):
#         try:
#             """Add the Missing and Found IDs sheet."""
#             ws = wb.active
#             ws.title = "Missing and Found IDs"

#             # Metadata Headers
#             header_font = Font(bold=True)
#             ws["A1"], ws["B1"] = "Current Date:", self.db_date
#             ws["A2"], ws["B2"] = "Folder Processed:", self.current_date
#             ws["A3"], ws["B3"] = "Total IDs Count:", len(db_letter_ids)
#             ws["A4"], ws["B4"] = "Found IDs Count:", len(ids_found)
#             ws["A5"], ws["B5"] = "Missing IDs Count:", len(id_not_found)

#             # Apply Header Font
#             for cell in ["A1", "A2", "A3", "A4", "A5"]:
#                 ws[cell].font = header_font

#             # Column Headers
#             ws["A7"], ws["B7"] = "Missing IDs", "Found IDs"
#             ws["A7"].font = ws["B7"].font = header_font

#             # Populate Data
#             for i, missing_id in enumerate(id_not_found, start=8):
#                 ws[f"A{i}"] = missing_id

#             for i, found_id in enumerate(ids_found, start=8):
#                 ws[f"B{i}"] = found_id

#             # Auto-Adjust Column Widths
#             for col in ws.columns:
#                 max_length = max((len(str(cell.value)) if cell.value else 0) for cell in col)
#                 col_letter = col[0].column_letter  # Get the column letter
#                 ws.column_dimensions[col_letter].width = max_length + 5
#         except Exception as e:
#             message = f"Exception in add_missing_and_found_sheet {e}"
#             traceback.print_exc()
#             self.logger.log_error(message)


#     def add_intra_doc_duplicates_sheet(self, wb, intra_doc_duplicates):
#         try:
#             """Add the Intra Doc Duplicates sheet."""
#             ws = wb.create_sheet(title="Intra Doc Duplicates")

#             # Headers
#             header_font = Font(bold=True)

#             ws["A1"], ws["B1"] = "Duplicate IDs Count:", sum([len(val) for key, val in intra_doc_duplicates.items()])
#             ws["A1"].font = ws["B1"].font = header_font


#             ws["A3"], ws["B3"], ws["D3"] = "Document", "Duplicate IDs", "Summary"
#             ws["A3"].font = ws["B3"].font = ws["D3"].font = header_font

#             # Populate Data
#             row = 4
#             for doc, duplicates in intra_doc_duplicates.items():
#                 duplicate_ids = ", ".join(duplicates)
#                 summary = f"{doc}.doc: {len(duplicates)} duplicates - IDs: {duplicate_ids}"
#                 ws[f"A{row}"] = f"{doc}.doc"
#                 ws[f"B{row}"] = duplicate_ids
#                 ws[f"D{row}"] = summary
#                 row += 1

#             # Auto-Adjust Column Widths
#             for col in ws.columns:
#                 max_length = max((len(str(cell.value)) if cell.value else 0) for cell in col)
#                 col_letter = col[0].column_letter
#                 ws.column_dimensions[col_letter].width = max_length + 5
#         except Exception as e:
#             message = f"Exception in add_intra_doc_duplicates_sheet {e}"
#             traceback.print_exc()
#             self.logger.log_error(message)


#     def add_cross_doc_duplicates_sheet(self, wb, cross_doc_duplicates):
#         try:
#             """Add the Cross Doc Duplicates sheet."""
#             ws = wb.create_sheet(title="Cross Doc Duplicates")

#             # Headers
#             header_font = Font(bold=True)

#             ws["A1"], ws["B1"] = "Duplicate IDs Count:", len({letter_id for duplicates in cross_doc_duplicates.values() for letter_id, _ in duplicates})
#             ws["A1"].font = ws["B1"].font = header_font

#             ws["A3"], ws["B3"], ws["C3"], ws["E3"] = "Document", "Duplicate ID", "Linked Document/Found In", "Summary"
#             ws["A3"].font = ws["B3"].font = ws["C3"].font = ws["E3"].font = header_font

#             # Populate Data
#             row = 4
#             for doc, cross_dupes in cross_doc_duplicates.items():
#                 for duplicate_id, linked_document in cross_dupes:
#                     ws[f"A{row}"] = f"{doc}.doc"
#                     ws[f"B{row}"] = duplicate_id
#                     ws[f"C{row}"] = f"{linked_document}.doc"
#                     row += 1

#             row = 4
#             for doc, cross_dupes in cross_doc_duplicates.items():
#                 cross_ids = [f"{item[0]} (also in {item[1]}.doc)" for item in cross_dupes]
#                 summary = f"{doc}.doc: {len(cross_dupes)} duplicates - {', '.join(cross_ids)}"
#                 ws[f"E{row}"] = summary if summary else ""
#                 row += 1

#             # Auto-Adjust Column Widths
#             for col in ws.columns:
#                 max_length = max((len(str(cell.value)) if cell.value else 0) for cell in col)
#                 col_letter = col[0].column_letter
#                 ws.column_dimensions[col_letter].width = max_length + 5
#         except Exception as e:
#             message = f"Exception in add_cross_doc_duplicates_sheet {e}"
#             traceback.print_exc()
#             self.logger.log_error(message)
    

    