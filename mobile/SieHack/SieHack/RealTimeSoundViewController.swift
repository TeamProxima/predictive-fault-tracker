//
//  RealTimeSoundViewController.swift
//  SieHack
//
//  Created by Emre Yigit Alparslan on 10/23/16.
//  Copyright © 2016 Proxima. All rights reserved.
//

import UIKit

class RealTimeSoundViewController: UIViewController {

    @IBOutlet weak var problemLabel: UILabel!
    
    var timer = Timer()
    var rasIP = ""

    func updateChecks() {
        checkProblem()
    }
    
    func checkProblem(){
        let url = URL(string: "http://\(rasIP)/soundproblem")!
        let task = URLSession.shared.dataTask(with: url) { (data, response, error) in
            if error == nil{
                if let urlContent = data{
                    do{
                        let jsonResult = try JSONSerialization.jsonObject(with: urlContent, options: JSONSerialization.ReadingOptions.mutableContainers) as AnyObject
                        if let problem = jsonResult["problem"] as? Int{
                            let prob = problem 
                            DispatchQueue.main.sync(execute: {
                                if prob == 0{
                                    self.problemLabel.text = "There is not any unexpected situation."
                                    self.problemLabel.textColor = UIColor.green
                                }else{
                                    self.problemLabel.text = "We have an unexpected sound change on the machine."
                                    self.problemLabel.textColor = UIColor.red
                                }
                            })
                        }
                    }catch{
                        print("Json Process Failling")
                    }
                }
            }else{
                print(error)
            }
        }
        task.resume()
        
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }
    
    override func viewDidAppear(_ animated: Bool) {
        if let ri = UserDefaults.standard.value(forKey: "rasPi IP") as? String{
            rasIP = ri
        }
        updateChecks()
        timer = Timer.scheduledTimer(timeInterval: 2.5, target: self, selector: #selector(updateChecks), userInfo: nil, repeats: true)
    }
    
    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
