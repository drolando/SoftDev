%{
/**
 * This is a workaround for a minor swig bug when building on gcc 4.6.1 and above.
 * Prior to gcc 4.6.1 the STL headers like vector, string, etc. used to 
 * automatically pull in the cstddef header but starting with gcc 4.6.1 they no
 * longer do. This leads to swig generated a file that does not compile so we
 * explicitly include cstddef so the swig generated file will compile.
 */
#include <cstddef>
%}

%module(directors="1") fifechan


%include "std_string.i"

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

/*%include "exception.i"

%{
#define _FCN_EXC_HANDLER() \
	catch (fcn::Exception& _e) { \
		PyErr_Clear(); \
		char _err_line[12]; \
		sprintf(_err_line, ":%u", _e.getLine()); \
		std::string _err_msg = "Caught a gcn exception thrown in " + _e.getFilename() + _err_line + " in function " + _e.getFunction() + ": " + _e.getMessage(); \
		SWIG_exception(SWIG_RuntimeError, _err_msg.c_str()); \
	}
%}

%exception {
	try {
		$action
	}
	_FCN_EXC_HANDLER()
}
*/

%include engine/core/gui/fifechan/lib/fifechanlistener.i
%include engine/core/gui/fifechan/lib/widgets.i

