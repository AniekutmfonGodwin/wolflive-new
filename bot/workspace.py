
# %%
class workspace:

    def __init__(self):
        self.workspace = dict()
        # self.setup_workspace()
        


    def setup_workspace(self):
        self.default_workspace = self.workspace.copy()


    def update_workspace(self,*args, **kwargs):
        self.workspace = {**self.workspace,**kwargs}
        return {**self.workspace,**kwargs}
    
    def drop_workspace(self):
        self.workspace = self.default_workspace.copy()

# %%
