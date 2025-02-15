from injector import Injector

from anki_voc_extract.di.di_module import AnkiClientConfigModule, AnkiClientModule

injector = Injector([AnkiClientConfigModule(), AnkiClientModule()])
