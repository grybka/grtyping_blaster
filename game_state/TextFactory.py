import random

class TextFactory:
    def __init__(self):
        self.text_categories={}

    def load_text_category(self,category_name,file_path):
        with open(file_path,'r') as f:
            lines=f.readlines()
        text_list=[line.strip() for line in lines if line.strip()!='']
        self.text_categories[category_name]=text_list

    def generate_random_text(self,category_name):
        if category_name not in self.text_categories:
            raise Exception("Text category not found: "+category_name)
        return random.choice(self.text_categories[category_name])
    
    def generate_n_random_text(self,category_name,n):
        if category_name not in self.text_categories:
            raise Exception("Text category not found: "+category_name)
        chosen_words=[]
        for _ in range(n):
            my_choice=random.choice(self.text_categories[category_name])
            while my_choice in chosen_words:
                my_choice=random.choice(self.text_categories[category_name])
            chosen_words.append(my_choice)
        return chosen_words        