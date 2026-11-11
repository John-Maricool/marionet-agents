import 'dart:async';
import 'package:flutter/material.dart';

class OrderTrackingScreen extends StatefulWidget {
  const OrderTrackingScreen({super.key, required this.orderId, required this.api});
  final String orderId;
  final TrackingApi api;

  @override
  State<OrderTrackingScreen> createState() => _OrderTrackingScreenState();
}

class _OrderTrackingScreenState extends State<OrderTrackingScreen> {
  RiderPosition? _position;
  late StreamSubscription<RiderPosition> _sub;

  @override
  void initState() {
    super.initState();
    _sub = widget.api.riderPositions(widget.orderId).listen((p) {
      setState(() => _position = p);
    });
  }

  Future<void> _cancelOrder() async {
    await widget.api.cancel(widget.orderId);
    Navigator.of(context).pop(); // used after await
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Track order')),
      body: Center(child: Text(_position == null ? 'Waiting for rider' : '${_position!.lat}, ${_position!.lng}')),
      floatingActionButton: FloatingActionButton(onPressed: _cancelOrder, child: const Icon(Icons.close)),
    );
  }
  // Bug: no dispose(), subscription leaks.
}

class RiderPosition {
  RiderPosition(this.lat, this.lng);
  final double lat;
  final double lng;
}

abstract class TrackingApi {
  Stream<RiderPosition> riderPositions(String orderId);
  Future<void> cancel(String orderId);
}
