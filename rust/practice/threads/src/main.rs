use std::thread;
use std::time::Duration;

fn main() {
    let thread1 = thread::spawn(|| {
        for i in 1..30 {
            println!("Spawned thread val {}", i);
            thread::sleep(Duration::from_millis(100));
        }
    });

    for i in 1..20 {
        println!("Main thread val {}", i);
        thread::sleep(Duration::from_millis(100));
    }

    let res = thread1.join().unwrap();
    println!("Result {:?}", res);
}
