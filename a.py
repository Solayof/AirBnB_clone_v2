class Ch():
    city = "Hello world"
    
    @property
    def city(self, text):
        print(text)
        
    def __str__(self) -> str:
        return f"{self.city()}"
        
inst = Ch()
print(inst)
