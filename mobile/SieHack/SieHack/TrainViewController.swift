//
//  TrainViewController.swift
//  Siemens Hackathon2
//
//  Created by Emre Yigit Alparslan on 10/23/16.
//  Copyright © 2016 Proxima. All rights reserved.
//

import UIKit

class TrainViewController: UIViewController {

    @IBOutlet weak var trainSensor: UIButton!
    @IBOutlet weak var infoLabel: UILabel!
    @IBOutlet weak var alreadyTrainedLabel: UILabel!
    @IBOutlet weak var continueDashButton: UIButton!
    @IBOutlet weak var changeIPButton: UIButton!
    @IBOutlet weak var ipText: UITextField!
    @IBOutlet weak var submitButton: UIButton!
    
    var isStart = true
    var rasIP = ""
    
    @IBAction func submit(_ sender: AnyObject) {
        
        if (ipText.text)! != ""{
            UserDefaults.standard.set((ipText.text)!, forKey: "rasPi IP")
            rasIP = (ipText.text)!
            
            trainSensor.isHidden = false
            alreadyTrainedLabel.isHidden = false
            continueDashButton.isHidden = false
            changeIPButton.isHidden = false
            ipText.isHidden = true
            submitButton.isHidden = true
            
            view.endEditing(true)
        }
    }
    @IBAction func changeIP(_ sender: AnyObject) {
        trainSensor.isHidden = true
        alreadyTrainedLabel.isHidden = true
        continueDashButton.isHidden = true
        changeIPButton.isHidden = true
        ipText.isHidden = false
        submitButton.isHidden = false
    }
    @IBAction func trainTapped(_ sender: AnyObject) {
        if isStart == true{
            infoLabel.isHidden = false
            trainSensor.setTitle("Stop Training", for: [])
            changeIPButton.isHidden = true
            alreadyTrainedLabel.isHidden = true
            continueDashButton.isHidden = true
            isStart = false
        }else{
            sendTrainRequest()
            performSegue(withIdentifier: "toMainPage", sender: self)
        }
    }
    
    func sendTrainRequest(){
        
        let url = URL(string: "http://\(rasIP)/train")!
        let task = URLSession.shared.dataTask(with: url) { (data, response, error) in
            if error == nil{
                print("Train Stopped!")
            }else{
                print(error)
            }
        }
        task.resume()
    }

    func dismissKeyboard() {
        view.endEditing(true)
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let tap: UITapGestureRecognizer = UITapGestureRecognizer(target: self, action: #selector(TrainViewController.dismissKeyboard))
        view.addGestureRecognizer(tap)
        
        if UserDefaults.standard.value(forKey: "rasPi IP") != nil{
            rasIP = UserDefaults.standard.value(forKey: "rasPi IP") as! String
            
            trainSensor.isHidden = false
            alreadyTrainedLabel.isHidden = false
            continueDashButton.isHidden = false
            changeIPButton.isHidden = false
            ipText.isHidden = true
            submitButton.isHidden = true
        }
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
