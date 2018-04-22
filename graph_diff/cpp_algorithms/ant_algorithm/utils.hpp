#pragma once

#include <functional>
#include <tuple>


namespace std {

template <typename ...Args>
struct hash<std::tuple<Args...>> {
    size_t operator()(std::tuple<Args...> const& tup) const {
        constexpr static int N = sizeof...(Args);
        using int_seq = std::make_integer_sequence<size_t, N>;
        return Unpacker<int_seq>::unpack(tup);
    }

private:
    template <typename Int_seq>
    struct Unpacker{
        size_t static unpack(std::tuple<Args...> const& tup);
    };

    template <size_t ...I>
    struct Unpacker<std::integer_sequence<size_t, I...>> {
        size_t static unpack(std::tuple<Args...> const& tup) {
            return eval(std::get<I>(tup)...);
        }
    };

    template <typename T>
    size_t static eval_hash(T const& a) {
        return std::hash<T>()(a);
    }

    size_t static eval(Args const& ...args) {
        return ((eval_hash(args) * 239) + ...);
    }
};

} // end of namespace std