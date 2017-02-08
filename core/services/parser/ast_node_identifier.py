class ASTNodeId():
    @staticmethod
    def getNamespaceId():
        return "namespace"

    @staticmethod
    def getNamespaceAliasId():
        return "namespace_alias"

    @staticmethod
    def getClassId():
        return "class"

    @staticmethod
    def getStructId():
        return "struct"

    @staticmethod
    def getEnumId():
        return "enum"

    @staticmethod
    def getEnumValueId():
        return "enum_value"

    @staticmethod
    def getUnionId():
        return "union"

    @staticmethod
    def getFieldId():
        return "class_struct_union_field"

    @staticmethod
    def getLocalVariableId():
        return "local_variable"

    @staticmethod
    def getFunctionId():
        return "function"

    @staticmethod
    def getMethodId():
        return "method"

    @staticmethod
    def getFunctionParameterId():
        return "function_or_method_parameter"

    @staticmethod
    def getTemplateTypeParameterId():
        return "template_type_parameter"

    @staticmethod
    def getTemplateNonTypeParameterId():
        return "template_non_type_parameter"

    @staticmethod
    def getTemplateTemplateParameterId():
        return "template_template_parameter"

    @staticmethod
    def getMacroDefinitionId():
        return "macro_definition"

    @staticmethod
    def getMacroInstantiationId():
        return "macro_instantiation"

    @staticmethod
    def getTypedefId():
        return "typedef"

    @staticmethod
    def getUsingDirectiveId():
        return "using_directive"

    @staticmethod
    def getUsingDeclarationId():
        return "using_declaration"

    @staticmethod
    def getUnsupportedId():
        return "unsupported"

