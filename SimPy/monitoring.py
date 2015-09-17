from functools import partial, wraps


def monitor(data, resource):
    """This is our monitoring callback."""
    item = [
        resource._env.now,  # The current simulation time
        resource.count
        ]  #,resource._env._queue The number of users
        
    if len(resource.queue)>0:
        #print type(resource.queue[0])
        #print resource._env.now, [k.proc.target for k in resource.queue]
        pass#item.extend(resource.queue[0].machine)  # The number of queued processes'''
    '''if len(resource.users)>0:
        print type(resource.users[0])#'''

    data.append(item)


def patch_resource(resource, pre=None, post=None):
    def get_wrapper(func):
        # Generate a wrapper for put/get/request/release
        @wraps(func)
        def wrapper(*args, **kwargs):
            # This is the actual wrapper
            # Call "pre" callback
            if pre:
                pre(resource)
        
            # Perform actual operation
            ret = func(*args, **kwargs)
        
            # Call "post" callback
            if post:
                post(resource)
        
            return ret
        return wrapper

    # Replace the original operations with our wrapper
    for name in ['put', 'get', 'request', 'release']:
        if hasattr(resource, name):
            setattr(resource, name, get_wrapper(getattr(resource, name)))



