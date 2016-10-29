//
//  WeeklyTemperatureViewController.swift
//  Siemens Hackathon2
//
//  Created by Emre Yigit Alparslan on 10/23/16.
//  Copyright © 2016 Proxima. All rights reserved.
//

import UIKit
import Charts

class WeeklyTemperatureViewController: UIViewController {

    @IBOutlet weak var tempLineChart: LineChartView!
    @IBOutlet weak var humiLineChart: LineChartView!
    @IBOutlet weak var activityIndi: UIActivityIndicatorView!
    
    var rasIP = ""
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
        tempLineChart.noDataText = ""
        humiLineChart.noDataText = ""
        if let ri = UserDefaults.standard.value(forKey: "rasPi IP") as? String{
            rasIP = ri
        }
        getDataFromDatabase()
    }

    func setLineChart(element: String, values: [Double]) {
        
        var dataEntries: [ChartDataEntry] = []
        
        for i in 0..<values.count {
            let dataEntry = ChartDataEntry(x: Double(i), y: values[i])
            dataEntries.append(dataEntry)
        }
        
        if element == "Humidity"{
            
            let lineChartDataSet = LineChartDataSet(values: dataEntries, label: "Humidity")
            lineChartDataSet.circleRadius = 0.0
            lineChartDataSet.setColor(NSUIColor.green)
            let lineChartData = LineChartData(dataSet: lineChartDataSet)
            lineChartData.setDrawValues(false)
            humiLineChart.data = lineChartData
            humiLineChart.setScaleEnabled(true)
            
        }else if element == "Temperature"{
            
            let lineChartDataSet = LineChartDataSet(values: dataEntries, label: "Temperature")
            lineChartDataSet.circleRadius = 0.0
            lineChartDataSet.setColor(NSUIColor.red)
            let lineChartData = LineChartData(dataSet: lineChartDataSet)
            lineChartData.setDrawValues(false)
            tempLineChart.data = lineChartData
            tempLineChart.setScaleEnabled(true)
            
        }
        
    }
    
    func getDataFromDatabase(){
        
        tempLineChart.isUserInteractionEnabled = false
        humiLineChart.isUserInteractionEnabled = false
        activityIndi.isHidden = false
        activityIndi.startAnimating()
        
        let url = URL(string: "http://\(rasIP)/weekly")!
        let task = URLSession.shared.dataTask(with: url) { (data, response, error) in
            if error == nil{
                if let urlContent = data{
                    do{
                        let jsonResult = try JSONSerialization.jsonObject(with: urlContent, options: JSONSerialization.ReadingOptions.mutableContainers) as AnyObject
                        
                        var datasetTemp = [Double]()
                        var datasetHumi = [Double]()
                        
                        if let elements = (jsonResult["scores"])! as? NSArray{
                            var i = 0
                            while i < elements.count{
                                if let element = elements[i] as? AnyObject{
                                    datasetTemp.append(element["temperature"] as! Double)
                                    datasetHumi.append(element["humidity"] as! Double)
                                    i+=1
                                }
                            }
                        }
                        
                        DispatchQueue.main.sync(execute: {
                            self.setLineChart(element: "Temperature", values: datasetTemp)
                            self.setLineChart(element: "Humidity", values: datasetHumi)
                            self.tempLineChart.isUserInteractionEnabled = true
                            self.humiLineChart.isUserInteractionEnabled = true
                            self.activityIndi.isHidden = true
                            self.activityIndi.stopAnimating()
                        })
                        
                        
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
