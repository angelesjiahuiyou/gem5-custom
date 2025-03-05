/*#include "pybind11/pybind11.h"
#include "mem/cache/cache.hh"

namespace py = pybind11;

void
init_Cache(py::module &m)
{
    py::class_<Cache, BaseCache, std::unique_ptr<Cache, py::nodelete>>(m, "Cache")
        .def("printShiftStats", &Cache::printShiftStats,
             "Print the shift statistics (hit and miss) for the cache.");
}*/
