//
//  RealTimeTemperatureViewController.swift
//  Siemens Hackathon2
//
//  Created by Emre Yigit Alparslan on 10/23/16.
//  Copyright © 2016 Proxima. All rights reserved.
//

import UIKit
import Charts

class RealTimeTemperatureViewController: UIViewController {

    @IBOutlet weak var problemLabel: UILabel!
    @IBOutlet weak var lineChartRealTimeTemp: LineChartView!
    @IBOutlet weak var temperatureLabel: UILabel!
    @IBOutlet weak var humidityLabel: UILabel!
    
    var timer = Timer()
    var rasIP = ""
    
    func updateChecks() {
        getDataFromDatabase()
        checkProblem()
    }
    
    func checkProblem(){
        let url = URL(string: "http://\(rasIP)/tempproblem")!
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
                                    self.problemLabel.text = "We have an unexpected temperature change on the machine."
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
    
    func getDataFromDatabase(){
        let url = URL(string: "http://\(rasIP)/latest")!
        let task = URLSession.shared.dataTask(with: url) { (data, response, error) in
            if error == nil{
                if let urlContent = data{
                    do{
                        let jsonResult = try JSONSerialization.jsonObject(with: urlContent, options: JSONSerialization.ReadingOptions.mutableContainers) as AnyObject
                        if let temp = jsonResult["temperature"] as? Double{
                            if let hum = jsonResult["humidity"] as? Double{
                                DispatchQueue.main.sync(execute: {
                                    self.temperatureLabel.text = "\(temp)°C"
                                    self.humidityLabel.text = "%\(hum)"
                                })
                            }
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
    
    @IBAction func toDaily(_ sender: AnyObject) {
        timer.invalidate()
        performSegue(withIdentifier: "toDaily", sender: self)
    }
    @IBAction func toWeekly(_ sender: AnyObject) {
        timer.invalidate()
        performSegue(withIdentifier: "toWeekly", sender: self)
    }
    
    override func viewDidAppear(_ animated: Bool) {
        if let ri = UserDefaults.standard.value(forKey: "rasPi IP") as? String{
            rasIP = ri
        }
        
        updateChecks()
        timer = Timer.scheduledTimer(timeInterval: 2.5, target: self, selector: #selector(updateChecks), userInfo: nil, repeats: true)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view.
        
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
