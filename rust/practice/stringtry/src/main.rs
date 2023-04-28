fn main() {
    println!("String demo");

    let mut s1: String = String::new();

    s1.push_str("Rust");
    s1.push(' ');
    s1.push_str("World");

    for word in s1.split_whitespace() {
        println!("{}", word);
    }

    let s2: String = s1.replace("Rust", "Rusty");

    println!("{}", s2);

    string_try2();

    fn use_func<T>(a: i32, b: i32, func: T) -> i32
    where
        T: Fn(i32, i32) -> i32,
    {
        func(a, b)
    }

    let sum = |a: i32, b: i32| a + b;
    let prod = |a: i32, b: i32| a * b;

    println!("The sum is {:?}", use_func(5, 4, sum));
    println!("The prod is {:?}", use_func(5, 4, prod));
}

fn string_try2() {
    let s1: String = String::from("a h k l y b f g r e f f d g");
    let mut svec: Vec<char> = s1.chars().collect();

    svec.sort();
    svec.dedup();

    for char in svec {
        print!("{}", char);
    }

    let str = String::new();
    println!("{}", str);
}
