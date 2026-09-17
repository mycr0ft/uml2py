"""StandardProfile stereotype classes generated from the OMG profile XMI.

33 stereotypes, 0 tagged values, 0 constraints
(metadata). Stereotypes fold their base metaclasses (Python inheritance)
with stereotype generalizations; base_* extension ends are consumed;
extension required/optional data is in _EXTENSIONS.
"""
from __future__ import annotations

import enum as _enum

from gen import uml25 as U
from gen.uml25 import _Ref  # noqa: F401

_URI = None  # profile XMI carries no <URI>; applied URI is dialect-dependent


class Auxiliary(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Auxiliary"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class BuildComponent(U.Component):
    _STEREO = "StandardProfile::StandardProfile::BuildComponent"
    _BASE_METACLASSES = ("Component",)
    _ABSTRACT = False

class Call(U.Usage):
    _STEREO = "StandardProfile::StandardProfile::Call"
    _BASE_METACLASSES = ("Usage",)
    _ABSTRACT = False

class Create(U.Usage, U.BehavioralFeature):
    _STEREO = "StandardProfile::StandardProfile::Create"
    _BASE_METACLASSES = ("BehavioralFeature", "Usage",)
    _ABSTRACT = False

class Derive(U.Abstraction):
    _STEREO = "StandardProfile::StandardProfile::Derive"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False

class Destroy(U.BehavioralFeature):
    _STEREO = "StandardProfile::StandardProfile::Destroy"
    _BASE_METACLASSES = ("BehavioralFeature",)
    _ABSTRACT = False

class File(U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::File"
    _BASE_METACLASSES = ("Artifact",)
    _ABSTRACT = False

class Document(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Document"
    _BASE_METACLASSES = ("Artifact",)
    _ABSTRACT = False

class Entity(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Entity"
    _BASE_METACLASSES = ("Component",)
    _ABSTRACT = False

class Executable(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Executable"
    _BASE_METACLASSES = ("Artifact",)
    _ABSTRACT = False

class Focus(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Focus"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Framework(U.Package):
    _STEREO = "StandardProfile::StandardProfile::Framework"
    _BASE_METACLASSES = ("Package",)
    _ABSTRACT = False

class Implement(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Implement"
    _BASE_METACLASSES = ("Component",)
    _ABSTRACT = False

class ImplementationClass(U.Class):
    _STEREO = "StandardProfile::StandardProfile::ImplementationClass"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Instantiate(U.Usage):
    _STEREO = "StandardProfile::StandardProfile::Instantiate"
    _BASE_METACLASSES = ("Usage",)
    _ABSTRACT = False

class Library(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Library"
    _BASE_METACLASSES = ("Artifact",)
    _ABSTRACT = False

class Metaclass(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Metaclass"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Metamodel(U.Model):
    _STEREO = "StandardProfile::StandardProfile::Metamodel"
    _BASE_METACLASSES = ("Model",)
    _ABSTRACT = False

class ModelLibrary(U.Package):
    _STEREO = "StandardProfile::StandardProfile::ModelLibrary"
    _BASE_METACLASSES = ("Package",)
    _ABSTRACT = False

class Process(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Process"
    _BASE_METACLASSES = ("Component",)
    _ABSTRACT = False

class Realization(U.Classifier):
    _STEREO = "StandardProfile::StandardProfile::Realization"
    _BASE_METACLASSES = ("Classifier",)
    _ABSTRACT = False

class Refine(U.Abstraction):
    _STEREO = "StandardProfile::StandardProfile::Refine"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False

class Responsibility(U.Usage):
    _STEREO = "StandardProfile::StandardProfile::Responsibility"
    _BASE_METACLASSES = ("Usage",)
    _ABSTRACT = False

class Script(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Script"
    _BASE_METACLASSES = ("Artifact",)
    _ABSTRACT = False

class Send(U.Usage):
    _STEREO = "StandardProfile::StandardProfile::Send"
    _BASE_METACLASSES = ("Usage",)
    _ABSTRACT = False

class Service(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Service"
    _BASE_METACLASSES = ("Component",)
    _ABSTRACT = False

class Source(File, U.Artifact):
    _STEREO = "StandardProfile::StandardProfile::Source"
    _BASE_METACLASSES = ("Artifact",)
    _ABSTRACT = False

class Specification(U.Classifier):
    _STEREO = "StandardProfile::StandardProfile::Specification"
    _BASE_METACLASSES = ("Classifier",)
    _ABSTRACT = False

class Subsystem(U.Component):
    _STEREO = "StandardProfile::StandardProfile::Subsystem"
    _BASE_METACLASSES = ("Component",)
    _ABSTRACT = False

class SystemModel(U.Model):
    _STEREO = "StandardProfile::StandardProfile::SystemModel"
    _BASE_METACLASSES = ("Model",)
    _ABSTRACT = False

class Trace(U.Abstraction):
    _STEREO = "StandardProfile::StandardProfile::Trace"
    _BASE_METACLASSES = ("Abstraction",)
    _ABSTRACT = False

class Type(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Type"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

class Utility(U.Class):
    _STEREO = "StandardProfile::StandardProfile::Utility"
    _BASE_METACLASSES = ("Class",)
    _ABSTRACT = False

# ---------------------------------------------------------------------------
# post-import assembly (mirror of uml25._finish for stereotype classes)
# ---------------------------------------------------------------------------
_STEREOTYPES = [Auxiliary, BuildComponent, Call, Create, Derive, Destroy, File, Document, Entity, Executable, Focus, Framework, Implement, ImplementationClass, Instantiate, Library, Metaclass, Metamodel, ModelLibrary, Process, Realization, Refine, Responsibility, Script, Send, Service, Source, Specification, Subsystem, SystemModel, Trace, Type, Utility]
_EXTENSIONS = {
    "Auxiliary": (("Class", False),),
    "BuildComponent": (("Component", False),),
    "Call": (("Usage", False),),
    "Create": (("BehavioralFeature", False), ("Usage", False),),
    "Derive": (("Abstraction", False),),
    "Destroy": (("BehavioralFeature", False),),
    "Document": (("Artifact", False),),
    "Entity": (("Component", False),),
    "Executable": (("Artifact", False),),
    "File": (("Artifact", False),),
    "Focus": (("Class", False),),
    "Framework": (("Package", False),),
    "Implement": (("Component", False),),
    "ImplementationClass": (("Class", False),),
    "Instantiate": (("Usage", False),),
    "Library": (("Artifact", False),),
    "Metaclass": (("Class", False),),
    "Metamodel": (("Model", False),),
    "ModelLibrary": (("Package", False),),
    "Process": (("Component", False),),
    "Realization": (("Classifier", False),),
    "Refine": (("Abstraction", False),),
    "Responsibility": (("Usage", False),),
    "Script": (("Artifact", False),),
    "Send": (("Usage", False),),
    "Service": (("Component", False),),
    "Source": (("Artifact", False),),
    "Specification": (("Classifier", False),),
    "Subsystem": (("Component", False),),
    "SystemModel": (("Model", False),),
    "Trace": (("Abstraction", False),),
    "Type": (("Class", False),),
    "Utility": (("Class", False),),
}

def _finish():
    for c in _STEREOTYPES:
        decl = c.__dict__.get('_DECL')
        if not decl:
            continue
        for d in decl.values():
            d.owner_cls = c.__name__
        for n, d in decl.items():
            setattr(c, n, d)
_finish()

