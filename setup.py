#################################################################################
#
# (c) Copyright 2010 William Stein
#
#  This file is part of PSAGE
#
#  PSAGE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  PSAGE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################


import os, sys

import build_system

SAGE_ROOT = os.environ['SAGE_ROOT']

INCLUDES = ['%s/%s/'%(SAGE_ROOT,x) for x in
            ['local/include/csage', 'local/include', 'local/include/python2.6/',
             'devel/sage/sage/ext', 'devel/sage', 'devel/sage/sage/gsl']]

if '-ba' in sys.argv:
    print "Rebuilding all Cython extensions."
    FORCE = True
else:
    FORCE = False

def Extension(*args, **kwds):
    if not kwds.has_key('include_dirs'):
        kwds['include_dirs'] = INCLUDES
    else:
        kwds['include_dirs'] += INCLUDES
    if not kwds.has_key('force'):
        kwds['force'] = FORCE

    # Disable warnings when running GCC step -- cython has already parsed the code and
    # generated any warnings; the GCC ones are noise.
    if not kwds.has_key('extra_compile_args'):
        kwds['extra_compile_args'] = ['-w']
    else:
        kwds['extra_compile_args'].append('-w')
        
    E = build_system.Extension(*args, **kwds)
    E.libraries = ['csage'] + E.libraries
    return E


numpy_include_dirs = [os.path.join(SAGE_ROOT,
                                   'local/lib/python/site-packages/numpy/core/include')]

ext_modules = [
    Extension("psage.ellff.ellff",
              ["psage/ellff/ellff.pyx",
               "psage/ellff/ell.cpp",
               "psage/ellff/ell_surface.cpp",
               "psage/ellff/euler.cpp",
               "psage/ellff/helper.cpp",
               "psage/ellff/jacobi.cpp",
               "psage/ellff/lzz_pEExtra.cpp",
               "psage/ellff/lzz_pEratX.cpp"],
              language = 'c++'),
    
    Extension("psage.function_fields.function_field_element",
              ["psage/function_fields/function_field_element.pyx"]),
    
    Extension("psage.modform.siegel.fastmult",
              ["psage/modform/siegel/fastmult.pyx"]),

    Extension('psage.modform.maass.mysubgroups_alg',
              ['psage/modform/maass/mysubgroups_alg.pyx']),

    Extension('psage.modform.maass.maass_forms_alg',
              ['psage/modform/maass/maass_forms_alg.pyx'],
              include_dirs = numpy_include_dirs),

    Extension('psage.modform.maass.lpkbessel',
              ['psage/modform/maass/lpkbessel.pyx']),

    Extension("psage.modform.hilbert.sqrt5.sqrt5_fast",
              ["psage/modform/hilbert/sqrt5/sqrt5_fast.pyx"],
              libraries = ['gmp']),
    
    

]

build_system.cythonize(ext_modules)

build_system.setup(
    name = 'psage',
    version = "10.10.28",
    description = "PSAGE: Software for Arithmetic Geometry",
    author = 'William Stein',
    author_email = 'wstein@gmail.com',
    url = 'http://purple.sagemath.org',
    license = 'GPL v3+',
    packages = ['psage',
                'psage.ellff',
                'psage.function_fields',
                'psage.lmfdb',
                'psage.modform',
                'psage.modform.hilbert',
                'psage.modform.hilbert.sqrt5',
                'psage.modform.rational'],
    platforms = ['any'],
    download_url = 'NA',
    ext_modules = ext_modules
)

