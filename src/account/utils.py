from django.apps import apps 


def database_checker(app_name,model_name,**kwargs):
    """
        This is a function to check the existence of an object  
        in database  by its unqiue fields.
        we pass unqie fields name and thier values in kwargs. 
    """
    class_model=apps.get_model(app_label=app_name,model_name=model_name)
    obj=class_model.objects.filter(**kwargs)
    print("\n"*5,obj.count())
    if(obj.count()==0):
        return(False)
    return(True)