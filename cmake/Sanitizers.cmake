# SLAMBOT_SANITIZER=address builds everything with AddressSanitizer and
# UndefinedBehaviorSanitizer, SLAMBOT_SANITIZER=thread with ThreadSanitizer.
# The asan and tsan presets in CMakePresets.json set it, each in its own build
# folder.
set(SLAMBOT_SANITIZER "" CACHE STRING "Sanitizer to build with: address, thread or empty")
set_property(CACHE SLAMBOT_SANITIZER PROPERTY STRINGS "" address thread)

if(SLAMBOT_SANITIZER STREQUAL "address")
    # Make undefined behavior fail the test instead of only printing a warning.
    set(sanitizer_flags -fsanitize=address,undefined -fno-sanitize-recover=all)
elseif(SLAMBOT_SANITIZER STREQUAL "thread")
    set(sanitizer_flags -fsanitize=thread)
elseif(NOT SLAMBOT_SANITIZER STREQUAL "")
    message(FATAL_ERROR "Unknown SLAMBOT_SANITIZER '${SLAMBOT_SANITIZER}', use address or thread")
endif()

if(sanitizer_flags)
    # Debug info and frame pointers give readable stack traces in Release builds.
    add_compile_options(${sanitizer_flags} -g -fno-omit-frame-pointer)
    add_link_options(${sanitizer_flags})
endif()
