def swap_decorator(fn):#fn(sub(2,10))
    def wrapper(n1,n2):#n1=2,n2=10
        if n2>n1:#10>2
            (n1,n2)=(n2,n1)#(10,2)
        return fn(n1,n2)#sub(10,2)
    return wrapper
def sub(n1,n2):
    # if n2>n1:
    #     (n1,n2)=(n2,n1)
    return n1-n2
print(sub(10,2))
print(sub(2,10))

def sigin_required(fn)
    def wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

@fn name
def post(request,*args,**kwargs):
    return "some logic"