from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class RocksdbConan(ConanFile):
    name = "rocksdb"
    version = "6.6.4"
    url = "https://github.com/Zinnion/conan-rocksdb"
    description = "A library that provides an embeddable, persistent key-value store for fast storage"
    topics = ("conan", "rocksdb", "keyvalue")
    homepage = "https://github.com/facebook/rocksdb"
    author = "Zinnion <mauro@zinnion.com>"
    license = "GPL-2.0"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False] }
    default_options = {'shared': False }
    source_subfolder = "source_subfolder"

    def requirements(self):
        self.requires.add("OpenSSL/1.1.1d@zinnion/stable")
        self.requires.add("zlib/1.2.11@zinnion/stable")
        self.requires.add("bzip2/1.0.6@zinnion/stable")
        self.requires.add("lz4/1.8.3@zinnion/stable")
        self.requires.add("snappy/1.1.7@zinnion/stable")

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
        with tools.chdir(self.source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = True
            if self.options.shared:
                env_build.make(["shared_lib"])  # $ make shared_lib
            else:
                env_build.make(["static_lib"])  # $ make static_lib

    def package(self):
        self.copy("*.h", dst="include", src=("%s/include" % self.source_subfolder))
        if self.options.shared:
            self.copy("librocksdb.so", dst="lib", src=self.source_subfolder, keep_path=False)
        else:
            self.copy("librocksdb.a", dst="lib", src=self.source_subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
