import frappe
from frappe.model.document import Document


class ITAsset(Document):
    def before_save(self):
        """Log assignment changes automatically."""
        old_doc = self.get_doc_before_save()
        if not old_doc:
            # New record — log initial assignment if there is one
            if self.assigned_to_name:
                self.append("assignment_history", {
                    "assigned_to": self.assigned_to_name,
                    "assigned_date": frappe.utils.today(),
                    "action": "Assigned",
                })
            return

        # Check if assignment changed
        if old_doc.assigned_to_name != self.assigned_to_name:
            # Log the previous person being unassigned
            if old_doc.assigned_to_name:
                self.append("assignment_history", {
                    "assigned_to": old_doc.assigned_to_name,
                    "assigned_date": frappe.utils.today(),
                    "action": "Unassigned",
                })
            # Log the new person being assigned
            if self.assigned_to_name:
                self.append("assignment_history", {
                    "assigned_to": self.assigned_to_name,
                    "assigned_date": frappe.utils.today(),
                    "action": "Assigned",
                })
