use std::{env, path::Path, process};
use rxing::{self, Exceptions::NotFoundException};

fn usage() -> ! {
    eprintln!("usage: barcode-read [--first] <path-to-image>");
    process::exit(2);
}


pub enum ReturnBarcodes {
    First(Option<String>),
    List(Vec<String>)
}


pub enum GetBarcodes {
    Ok(ReturnBarcodes),
    Err(String),
    PathError
}

fn main() {
    let mut args = env::args().skip(1);

    let mut path: Option<String> = None;

    let first_only = match args.next() {
        Some(arg) if arg == "--first" => true,
        Some(p) => {
            path = Some(p);
            false
        }
        None => usage()
    };

    if let None = path {
        path = match args.next() {
            Some(p) => Some(p),
            None => usage()
        }
    };

    if path.is_none() {
        usage()
    }

    match read_barcodes(first_only, path.unwrap()) {
        GetBarcodes::Ok(barcodes) => {
            match barcodes {
                ReturnBarcodes::First(barcode) => 
                    match barcode {
                        Some(barcode) => println!("{}", barcode),
                        _ => eprintln!("No barcode found!")
                    }
                ,
                ReturnBarcodes::List(barcodes) => {
                    if !barcodes.is_empty() {
                        println!("{}", barcodes.join(";"));
                        return
                    }
                    eprintln!("No barcodes found!");
                }
            }
        },
        GetBarcodes::Err(error) => eprintln!("Error: '{}'", error),
        GetBarcodes::PathError => eprintln!("Path error!")
    }
}


fn read_barcodes(first_only: bool, path: String) -> GetBarcodes {
    let img_path = Path::new(&path);

    if !img_path.exists() {
        return GetBarcodes::PathError
    }
    
    match img_path.to_str() {
        Some(p) => {
            match rxing::helpers::detect_multiple_in_file(p) {
                Ok(barcodes) => {
                    if first_only {
                        return GetBarcodes::Ok(ReturnBarcodes::First(barcodes.first().map(|r| r.getText().to_string())));
                    }
                    return GetBarcodes::Ok(ReturnBarcodes::List(barcodes.iter().map(|r| r.getText().to_string()).collect()))
                }
                Err(e) => {
                    if matches!(e, NotFoundException(_)) {
                        if first_only {
                            return GetBarcodes::Ok(ReturnBarcodes::First(None))
                        }
                        return GetBarcodes::Ok(ReturnBarcodes::List(vec![]))
                    }
                    return GetBarcodes::Err(e.to_string())
                }
            }
        },
        _ => return GetBarcodes::PathError
    }
}