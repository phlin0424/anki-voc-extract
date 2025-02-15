from injector import Injector

from anki_voc_extract.di.di_module import AnkiClientModule, ConfigModule

injector = Injector([ConfigModule(), AnkiClientModule()])
