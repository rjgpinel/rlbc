def add_to_stack(elem, stack, shift=1):
    if stack is not None:
        stack[:-shift] = stack[shift:].clone()
        stack[-shift:] = elem.clone()
    return stack
