class FormIDHandler:
    def __init__(self):
        self.base_form_id = 0x01000ED3
        self.current_form_id = self.base_form_id

    def new_form_id(self):
        self.current_form_id += 1
        return self.current_form_id
        