class Ch():
    __state = "Hello world"
    
    @property
    def city(self):
        return self.__state
    
    # @city.setter
    # def city(self, text):
    #     self.__city = text
        
    def __str__(self) -> str:
        return self.city
    
    def func(self, text):
        self.city = text
        
        
inst = Ch()
inst.func("Python is cool")
print(inst)
