import os
from conans import ConanFile, CMake, tools

class IMGUIConan(ConanFile):
    name = "imgui"
    version = "1.74"
    license = "MIT"
    url = "https://github.com/dbagrat/conan-imgui"
    homepage = "https://github.com/ocornut/imgui"
    description = "Bloat-free Immediate Mode Graphical User interface for C++ with minimal dependencies"
    author = "<Bagrat Dabaghyan> <dbagrat@gmail.com>"
    topics = ("imgui", "gui", "graphical", "user interface")
    exports = ["LICENSE.md"]
    #short_paths = True  #windows MAX_PATH(260) limitation fix
    exports_sources = ["CMakeLists.txt", ]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def package_id(self):
        self.info.vs_toolset_incompatible()

    def source(self):
        tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="examples/imgui_impl_*", dst="misc/bindings", src=self._source_subfolder, keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.srcdirs = ["misc", ]
        self.cpp_info.libs = tools.collect_libs(self)
