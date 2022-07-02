
#[no_mangle]
pub extern fn fibonacci(n: i32) -> i32 {
    if n < 2 {
        n
    } else {
        fibonacci(n - 1) + fibonacci(n - 2)
    }
}

#[no_mangle]
pub extern fn prime(n: u32) -> u32 {
    if n == 0 {
        return 2
    }

    let m = n as usize;

    let mut primes = vec![3];
    let mut recent = 3;
    let mut count = 1;

    while count < m {
        recent += 2;
        let mut is_prime = true;

        for item in &primes {
            if recent % item == 0 {
                is_prime = false;
                break;
            }
        }

        if is_prime {
            primes.push(recent);
            count += 1;
        }
    }

    primes[m - 1]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_calculate_fib8() {
        let result = fibonacci(8);
        assert_eq!(result, 21);
    }

    #[test]
    fn it_calculate_fib5() {
        let result = fibonacci(5);
        assert_eq!(result, 5);
    }
}
