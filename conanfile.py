from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

# https://github.com/giorgioazzinnaro/rocksdb/blob/master/INSTALL.md

class RocksdbConan(ConanFile):
    name = "rocksdb"
    version = "5.8"
    license = "https://github.com/facebook/rocksdb/blob/master/COPYING"
    url = "https://github.com/giorgioazzinnaro/conan-RocksDB"
    description = "A library that provides an embeddable, persistent key-value store for fast storage."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    source_tgz = "https://github.com/facebook/rocksdb/archive/v%s.tar.gz" % version

    requires = (
        "zlib/1.2.11@conan/stable",
        "bzip2/1.0.6@conan/stable",
        "lz4/1.8.3@zinnion/stable"
    )

    def source(self):
        self.output.info("Downloading %s" %self.source_tgz)
        tools.download(self.source_tgz, "rocksdb.tar.gz")
        tools.unzip("rocksdb.tar.gz")
        os.remove("rocksdb.tar.gz")

    @property
    def subfolder(self):
        return "rocksdb-%s" % self.version

    def build(self):
        with tools.chdir(self.subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = True

            if self.settings.build_type == "Debug":
                env_build.make()  # $ make
            else:
                if self.options.shared:
                    env_build.make(["shared_lib"])  # $ make shared_lib
                else:
                    env_build.make(["static_lib"])  # $ make static_lib

    def package(self):
        pass

    def package_info(self):
        self.cpp_info.libs = ["rocksdb"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")
