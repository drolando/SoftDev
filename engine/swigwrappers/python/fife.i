%{
/**
 * HAVE_SNPRINTF is defined in several places.  This prevents the warning message
 * from appearing when compiling the swig interface.
 */
#ifdef HAVE_SNPRINTF
#undef HAVE_SNPRINTF
#endif

/**
 * This is a workaround for a minor swig bug when building on gcc 4.6.1 and above.
 * Prior to gcc 4.6.1 the STL headers like vector, string, etc. used to 
 * automatically pull in the cstddef header but starting with gcc 4.6.1 they no
 * longer do. This leads to swig generated a file that does not compile so we
 * explicitly include cstddef so the swig generated file will compile.
 */
#include <cstddef>
%}

%module(directors="1") fife
%import engine/swigwrappers/python/fifechan.i

%include "std_string.i"
%include "std_vector.i"
%include "std_pair.i"
%include "std_list.i"
%include "std_map.i"
%include "std_set.i"
%include "typemaps.i"
%include "exception.i"

/**
 * Some materials to understand exception handling:
 *
 * Basics about python exceptions:
 * 	http://docs.python.org/tut/node10.html
 * Python exception handling in C APIs
 * 	http://docs.python.org/api/exceptions.html
 * 	http://docs.python.org/api/exceptionHandling.html
 * SWIG exception handling
 * 	http://www.swig.org/Doc1.3/Customization.html#exception 
 * 	http://www.swig.org/Doc1.3/SWIGPlus.html#SWIGPlus_exception_specifications
 * 	http://www.swig.org/Doc1.3/Python.html#Python_nn36
 */

%feature("autodoc", "1");  // 0 == no param types, 1 == show param types

%{
#include "util/base/fife_stdint.h"
%}

/**
 * Integer definitions (See swigs stdint.i implementation)
 *
 */

/* Signed.  */
typedef signed char		int8_t;
typedef short int		int16_t;
typedef int			int32_t;
#if defined(SWIGWORDSIZE64)
typedef long int		int64_t;
#else
typedef long long int		int64_t;
#endif

/* Unsigned.  */
typedef unsigned char		uint8_t;
typedef unsigned short int	uint16_t;
typedef unsigned int		uint32_t;
#if defined(SWIGWORDSIZE64)
typedef unsigned long int	uint64_t;
#else
typedef unsigned long long int	uint64_t;
#endif

namespace std {
	%template(StringVector) vector<std::string>;
	%template(UintVector) vector<uint32_t>;
	%template(IntVector) vector<int32_t>;
	%template(FloatVector) vector<float>;
	%template(DoubleVector) vector<double>;
	%template(BoolVector) vector<bool>;

	%template(Uint16Uint16Pair) pair<uint16_t, uint16_t>;
	%template(Uint16Uint16PairVector) vector<std::pair<uint16_t, uint16_t> >;
};

%{
#include "util/base/exception.h"
static void handleDirectorException() {
	PyObject* exception = NULL;
	PyObject* value = NULL;
	PyObject* traceback = NULL;
	PyErr_Fetch(&exception, &value, &traceback);
	PyErr_NormalizeException(&exception, &value, &traceback);
	if (exception) {
		PySys_SetObject((char*)"last_type", exception);
		PySys_SetObject((char*)"last_value", value);
		PySys_SetObject((char*)"last_traceback", traceback);	
		
		PyObject* d = PyModule_GetDict (PyImport_AddModule ("__main__"));
		PyDict_SetItemString(d, "exc_type", exception);
		PyDict_SetItemString(d, "exc_value", value);
		PyDict_SetItemString(d, "exc_traceback", traceback ? traceback : Py_None);
		
		char buf[1024];
		sprintf (buf, "\n\
import traceback\n\
s = 'Traceback (most recent call last):\\n'\n\
for filename, line, function, text in traceback.extract_tb(exc_traceback):\n\
	s = s + ' File \"%%s\", line %%d, in %%s\\n    %%s' %% (filename, line, function, text)\n\
	if s[-1] != '\\n': s = s + '\\n'\n\
for l in traceback.format_exception_only(exc_type, exc_value):\n\
	s = s + l\n\
	if s[-1] != '\\n': s = s + '\\n'\n\
print s\n\
");
		PyObject* e = PyRun_String(buf, Py_file_input, d, d);
		if (!e) {
			PyErr_Print();
		}
		Py_XDECREF(e);
		Py_XDECREF(d);
		Py_XDECREF(exception);
		Py_XDECREF(value);
		Py_XDECREF(traceback);
	}
}

#define _FIFE_EXC_HANDLER(_fife_exc_type, _converted_type) \
	catch (FIFE::_fife_exc_type& _e) { \
		PyErr_Clear(); \
		SWIG_exception(_converted_type, _e.what()); \
	}


#define _FIFE_DIRECTOR_EXC_HANDLER() \
	catch (Swig::DirectorException &) { \
		PyErr_Clear(); \
		SWIG_exception(SWIG_RuntimeError, "Caught a director exception"); \
	}
%}

%exceptionclass FIFE::Exception;

%feature("director:except") {
	if ($error != NULL) {
		handleDirectorException();
		throw Swig::DirectorMethodException();
	}
}

%exception {
	try {
		$action
	}
	_FIFE_DIRECTOR_EXC_HANDLER()
	_FIFE_EXC_HANDLER(Exception, SWIG_RuntimeError)
}

%include engine/core/audio/soundclip.i
%include engine/core/audio/soundclipmanager.i
%include engine/core/audio/soundemitter.i
%include engine/core/audio/soundmanager.i
%include engine/core/controller/engine.i
%include engine/core/eventchannel/eventchannel.i
%include engine/core/gui/fifechan/base/gui_font.i
%include engine/core/gui/fifechan/base/gui_image.i
%include engine/core/gui/fifechan/console/console.i
%include engine/core/gui/fifechan/fifechanmanager.i
%include engine/core/gui/fifechan/widgets/widgets.i
%include engine/core/gui/guimanager.i
%include engine/core/gui/hybrid/hybridguimanager.i
%include engine/core/loaders/native/map/ianimationloader.i
%include engine/core/loaders/native/map/iatlasloader.i
%include engine/core/loaders/native/map/imaploader.i
%include engine/core/loaders/native/map/iobjectloader.i
%include engine/core/loaders/native/map/maploader.i
%include engine/core/loaders/native/map/percentdonelistener.i
%include engine/core/model/metamodel/action.i
%include engine/core/model/metamodel/grids/cellgrids.i
%include engine/core/model/metamodel/ipather.i
%include engine/core/model/metamodel/ivisual.i
%include engine/core/model/metamodel/modelcoords.i
%include engine/core/model/metamodel/object.i
%include engine/core/model/metamodel/timeprovider.i
%include engine/core/model/model.i
%include engine/core/model/structures/cell.i
%include engine/core/model/structures/cellcache.i
%include engine/core/model/structures/instance.i
%include engine/core/model/structures/layer.i
%include engine/core/model/structures/location.i
%include engine/core/model/structures/map.i
%include engine/core/model/structures/renderernode.i
%include engine/core/model/structures/trigger.i
%include engine/core/pathfinder/route.i
%include engine/core/pathfinder/routepather/routepather.i
%include engine/core/savers/native/map/ianimationsaver.i
%include engine/core/savers/native/map/iatlassaver.i
%include engine/core/savers/native/map/imapsaver.i
%include engine/core/savers/native/map/iobjectsaver.i
%include engine/core/savers/native/map/mapsaver.i
%include engine/core/util/base/utilbase.i
%include engine/core/util/log/logger.i
%include engine/core/util/math/math.i
%include engine/core/util/resource/resource.i
%include engine/core/util/structures/utilstructures.i
%include engine/core/util/time/timeevent.i
%include engine/core/util/time/timemanager.i
%include engine/core/version.i
%include engine/core/vfs/raw/rawdata.i
%include engine/core/vfs/vfs.i
%include engine/core/video/fonts/fonts.i
%include engine/core/video/video.i
%include engine/core/view/camera.i
%include engine/core/view/rendererbase.i
%include engine/core/view/renderers/blockinginforenderer.i
%include engine/core/view/renderers/cellrenderer.i
%include engine/core/view/renderers/cellselectionrenderer.i
%include engine/core/view/renderers/coordinaterenderer.i
%include engine/core/view/renderers/floatingtextrenderer.i
%include engine/core/view/renderers/genericrenderer.i
%include engine/core/view/renderers/gridrenderer.i
%include engine/core/view/renderers/instancerenderer.i
%include engine/core/view/renderers/lightrenderer.i
%include engine/core/view/renderers/offrenderer.i
%include engine/core/view/renderers/targetrenderer.i
%include engine/core/view/visual.i

%include engine/swigwrappers/python/extensions.i.templ
