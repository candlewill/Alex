from collections import defaultdict

'''
特征向量相关的通用代码
'''


# TODO Extract the InstantiableI.
class Abstracted(object):
    other_val = "[OTHER]"
    splitter = "="

    # TODO Document.
    def __init__(self):
        """It is important for extending classes to call this initialiser."""
        self.instantiable = {self: self}
        self.is_generic = False

    def join_typeval(self, type_, val):
        return self.splitter.join((type_, val))

    def replace_typeval(self, combined, replacement):
        # TODO Document.
        raise NotImplementedError("This is an abstract method.")

    @classmethod
    def make_other(cls, type_):
        return u'{t}-OTHER'.format(t=type_)

    def iter_typeval(self):
        """Iterates the abstracted items in self, yielding combined
        representations of the type and value of each such token.  An abstract
        method of this class.

        """
        raise NotImplementedError('This is an abstract method.')

    def iter_triples(self):
        for combined_el in self.iter_typeval():
            split = combined_el.split(self.splitter, 2)
            try:
                type_, value = split
            except ValueError:
                value = ''
                type_ = split[0] if combined_el else ''
            # XXX Change the order of return values to combined_el, type_,
            # value.
            yield combined_el, value, type_

    # TODO Rename to something like iter_type_value.
    def iter_instantiations(self):
        types = set()
        for comb, value, type_ in self.iter_triples():
            types.add(type_)
            yield type_, value
        # Construct the other-instantiations for each type yet.
        # FIXME: Is this the correct thing to do?
        for type_ in types:
            yield type_, self.other_val

    def insts_for_type(self, type_):
        return [inst for inst in self.iter_instantiations()
                if inst[0] == type_]

    def insts_for_typeval(self, type_, value):
        same_type = [inst for inst in self.iter_instantiations()
                     if inst[0] == type_]
        # If self is not instantiable for type_,
        if not same_type:
            return same_type  # an empty list
        # If self knows the instantiation asked for,
        if (type_, value) in same_type:
            return [(type_, value)]
        # Else, instantiate with <other> as the value for `type_'.
        return [(type_, self.other_val)]

    def get_generic(self):
        new_combined = self
        type_counts = defaultdict(int)
        for combined, value, type_ in set(self.iter_triples()):
            if type_:
                new_combined = new_combined.replace_typeval(
                    combined,
                    self.join_typeval(type_, str(type_counts[type_])))
                type_counts[type_] += 1
                new_combined.is_generic = True
        return new_combined

    def get_concrete(self):
        ret = self
        for comb, value, type_ in self.iter_triples():
            ret = ret.replace_typeval(comb, value)
        return ret

    def instantiate(self, type_, value, do_abstract=False):
        """Example: Let self represent
            da1(a1=T1:v1)&da2(a2=T2:v2)&da3(a3=T1:v3).

        Calling      self.instantiate("T1", "v1")
        results in

            da1(a1=T1)&da2(a2=v2)&da3(a3=v3) ..if do_abstract == False

            da1(a1=T1)&da2(a2=v2)&da3(a3=T1_other) ..if do_abstract == True

        Calling      self.instantiate("T1", "x1")
        results in

            da1(a1=x1)&da2(a2=v2)&da3(a3=v3) ..if do_abstract == False

            da1(a1=T1_other)&da2(a2=v2)&da3(a3=T1_other)
                ..if do_abstract == True.

        """
        ret = self
        for combined, fld_value, fld_type in self.iter_triples():
            if type_ == fld_type:
                if value == fld_value:
                    ret = ret.replace_typeval(combined, type_)
                else:
                    if do_abstract:
                        ret = ret.replace_typeval(combined,
                                                  self.join_typeval(type_, self.make_other(type_)))
                    else:
                        ret = ret.replace_typeval(combined,
                                                  self.join_typeval(type_, fld_value))
            elif do_abstract:
                ret = ret.replace_typeval(combined, fld_type)
        return ret

    def all_instantiations(self, do_abstract=False):
        insts = set()
        for type_, value in self.iter_instantiations():
            inst = self.instantiate(type_, value, do_abstract)
            if inst not in insts:
                yield inst
                insts.add(inst)
        if not insts:
            yield self

    # XXX Is this used anywhere?
    def to_other(self):
        ret = self
        for combined, value, type_ in self.iter_triples():
            ret = ret.replace_typeval(combined, self.make_other(type_))
        return ret
