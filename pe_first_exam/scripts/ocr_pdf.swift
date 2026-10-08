import Foundation
import Vision
import CoreGraphics
import ImageIO

// Usage: ocr_pdf input.pdf output_dir [first_page] [last_page]
let args = CommandLine.arguments
guard args.count >= 3 else { fatalError("input.pdf output_dir required") }
let input = URL(fileURLWithPath: args[1])
let output = URL(fileURLWithPath: args[2], isDirectory: true)
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
guard let document = CGPDFDocument(input as CFURL) else { fatalError("Cannot open PDF") }
let first = args.count > 3 ? Int(args[3])! : 1
let last = args.count > 4 ? Int(args[4])! : document.numberOfPages
for number in first...last {
    let jsonURL = output.appendingPathComponent(String(format: "page_%03d.json", number))
    if FileManager.default.fileExists(atPath: jsonURL.path) { continue }
    try autoreleasepool {
        guard let page = document.page(at: number) else { fatalError("Missing page") }
        let box = page.getBoxRect(.mediaBox)
        let scale: CGFloat = 200.0 / 72.0
        let width = Int(box.width * scale), height = Int(box.height * scale)
        guard let context = CGContext(data: nil, width: width, height: height,
                bitsPerComponent: 8, bytesPerRow: 0, space: CGColorSpaceCreateDeviceRGB(),
                bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue) else { fatalError("Cannot render") }
        context.setFillColor(CGColor(gray: 1, alpha: 1))
        context.fill(CGRect(x: 0, y: 0, width: width, height: height))
        context.scaleBy(x: scale, y: scale)
        context.drawPDFPage(page)
        guard let image = context.makeImage() else { fatalError("Cannot make image") }
        let request = VNRecognizeTextRequest()
        request.recognitionLevel = .accurate
        request.recognitionLanguages = ["ja-JP", "en-US"]
        request.usesLanguageCorrection = false
        try VNImageRequestHandler(cgImage: image).perform([request])
        let observations = request.results ?? []
        let lines: [[String: Any]] = observations.compactMap { item in
            guard let text = item.topCandidates(1).first else { return nil }
            return ["text": text.string, "confidence": text.confidence,
                    "x": item.boundingBox.minX, "y": item.boundingBox.minY,
                    "width": item.boundingBox.width, "height": item.boundingBox.height]
        }
        let result: [String: Any] = ["page": number, "page_count": document.numberOfPages,
            "engine": "Apple Vision VNRecognizeTextRequest accurate ja-JP en-US",
            "render_dpi": 200, "lines": lines]
        let json = try JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys])
        try json.write(to: jsonURL)
        let pngURL = output.appendingPathComponent(String(format: "page_%03d.png", number))
        if let destination = CGImageDestinationCreateWithURL(pngURL as CFURL, "public.png" as CFString, 1, nil) {
            CGImageDestinationAddImage(destination, image, nil)
            if !CGImageDestinationFinalize(destination) { fatalError("Cannot save PNG") }
        }
        print("\(input.lastPathComponent) page \(number)/\(document.numberOfPages)")
    }
}
